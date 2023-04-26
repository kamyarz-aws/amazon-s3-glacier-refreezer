"""
Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
SPDX-License-Identifier: Apache-2.0
"""

import functools
import re
from typing import Any

from aws_cdk import Stack, Stage, Aws
from aws_cdk import aws_codebuild as codebuild
from aws_cdk import aws_codecommit as codecommit
from aws_cdk import pipelines
from aws_cdk import aws_iam as iam
from aws_cdk import aws_s3 as s3
from constructs import Construct

from refreezer.infrastructure.stack import RefreezerStack
from refreezer.mocking.mock_glacier_stack import MockGlacierStack

DEPLOY_STAGE_NAME = "test"
REFREEZER_STACK_NAME = "refreezer"
MOCK_GLACIER_STACK_NAME = "mock-glacier"
RESOURCE_NAME_LENGTH_LIMIT = 30


class PipelineStack(Stack):
    """
    This stack establishes a pipeline that builds, deploys, and tests the solution
    in a specified account. It uses a CodeCommit repo specified by context input
    to trigger the pipeline.

    The repo is configured using context parameters, specifically the following:

       - repository_name
          - CodeCommit repository name
       - branch
          - Branch to trigger the pipeline from
    """

    repository_name: str = "GlacierReFreezer"
    branch: str = "main"

    def __init__(self, scope: Construct, construct_id: str) -> None:
        context_repo = scope.node.try_get_context("repository_name")
        if context_repo:
            self.repository_name = context_repo
        context_branch = scope.node.try_get_context("branch")
        if context_branch:
            self.branch = context_branch

        super().__init__(
            scope, construct_id, stack_name=self.get_resource_name("pipeline")
        )

        cache_bucket = s3.Bucket(self, "CacheBucket")

        pipeline = pipelines.CodePipeline(
            self,
            "Pipeline",
            pipeline_name=self.get_resource_name("Pipeline"),
            synth=self.get_synth_step(cache_bucket),
            code_build_defaults=pipelines.CodeBuildOptions(
                build_environment=codebuild.BuildEnvironment(
                    build_image=codebuild.LinuxBuildImage.STANDARD_7_0,
                    compute_type=codebuild.ComputeType.LARGE,
                )
            ),
        )

        deploy_stage = DeployStage(self, self.get_resource_name(DEPLOY_STAGE_NAME))
        pipeline.add_stage(
            deploy_stage,
            post=[self.get_integration_test_step()],
        )

    def get_resource_name(self, name: str) -> str:
        """
        Returns a name with the repo and branch appended to differentiate pipelines between branches
        """
        concatenated = re.sub(r"[^a-zA-Z0-9-]+", "", f"{name}-grf-{self.branch}")
        checksum = functools.reduce(
            lambda a, b: a ^ b,
            bytes(f"{self.repository_name}{self.branch}", "utf-8"),
        )
        return f"{concatenated[:RESOURCE_NAME_LENGTH_LIMIT - 2]}{checksum:02x}"

    def get_connection(self) -> pipelines.CodePipelineSource:
        return pipelines.CodePipelineSource.code_commit(
            repository=codecommit.Repository.from_repository_name(
                scope=self,
                id="CodeCommitSource",
                repository_name=self.repository_name,
            ),
            branch=self.branch,
        )

    def get_synth_step(self, cache_bucket: s3.IBucket) -> pipelines.CodeBuildStep:
        return pipelines.CodeBuildStep(
            "Synth",
            input=self.get_connection(),
            env=dict(
                REPOSITORY_NAME=self.repository_name,
                BRANCH=self.branch,
            ),
            install_commands=[
                'pip install ".[dev]"',
            ],
            commands=[
                "tox --recreate --parallel-no-spinner -- --junitxml=pytest-report.xml",
                "npx cdk synth -c repository_name=$REPOSITORY_NAME -c branch=$BRANCH",
            ],
            partial_build_spec=self.get_partial_build_spec(
                dict(
                    reports=self.get_reports_build_spec_mapping("pytest-report.xml"),
                    cache=dict(
                        paths=[
                            ".mypy_cache/**/*",
                            ".tox/**/*",
                            "/root/.cache/pip/**/*",
                        ]
                    ),
                )
            ),
            cache=codebuild.Cache.bucket(cache_bucket),
        )

    def get_integration_test_step(self) -> pipelines.CodeBuildStep:
        stack_name = (
            f"{self.get_resource_name(DEPLOY_STAGE_NAME)}-{REFREEZER_STACK_NAME}"
        )
        return pipelines.CodeBuildStep(
            "IntegrationTest",
            install_commands=[
                "pip install tox",
            ],
            env=dict(STACK_NAME=stack_name),
            commands=["tox -e integration -- --junitxml=pytest-integration-report.xml"],
            role_policy_statements=[
                iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    actions=["cloudformation:DescribeStacks"],
                    resources=[
                        f"arn:aws:cloudformation:{Aws.REGION}:{Aws.ACCOUNT_ID}:stack/{stack_name}/*"
                    ],
                ),
                iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    actions=[
                        "dynamodb:GetItem",
                        "dynamodb:PutItem",
                        "dynamodb:DeleteItem",
                    ],
                    resources=[
                        f"arn:aws:dynamodb:{Aws.REGION}:{Aws.ACCOUNT_ID}:table/{stack_name}-*"
                    ],
                ),
                iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    actions=["sns:Publish", "sns:ListSubscriptionsByTopic"],
                    resources=[
                        f"arn:aws:sns:{Aws.REGION}:{Aws.ACCOUNT_ID}:{stack_name}-*"
                    ],
                ),
                iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    actions=["s3:PutObject", "s3:DeleteObject", "s3:GetObject"],
                    resources=[
                        f"arn:aws:s3:::{stack_name}-*",
                    ],
                ),
                iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    actions=[
                        "states:StartExecution",
                        "states:DescribeExecution",
                        "states:GetExecutionHistory",
                    ],
                    resources=[
                        f"arn:aws:states:{Aws.REGION}:{Aws.ACCOUNT_ID}:stateMachine:InventoryRetrievalStateMachine*",
                        f"arn:aws:states:{Aws.REGION}:{Aws.ACCOUNT_ID}:execution:InventoryRetrievalStateMachine*",
                        f"arn:aws:states:{Aws.REGION}:{Aws.ACCOUNT_ID}:stateMachine:InitiateRetrievalStateMachine*",
                        f"arn:aws:states:{Aws.REGION}:{Aws.ACCOUNT_ID}:execution:InitiateRetrievalStateMachine*",
                        f"arn:aws:states:{Aws.REGION}:{Aws.ACCOUNT_ID}:stateMachine:RetrieveArchiveStateMachine*",
                        f"arn:aws:states:{Aws.REGION}:{Aws.ACCOUNT_ID}:execution:RetrieveArchiveStateMachine*",
                    ],
                ),
                iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    actions=["lambda:InvokeFunction", "lambda:GetFunction"],
                    resources=[
                        f"arn:aws:lambda:{Aws.REGION}:{Aws.ACCOUNT_ID}:function:{stack_name}-*"
                    ],
                ),
            ],
            partial_build_spec=self.get_partial_build_spec(
                dict(
                    reports=self.get_reports_build_spec_mapping(
                        "pytest-integration-report.xml"
                    ),
                )
            ),
        )

    def get_partial_build_spec(self, mapping: dict[str, Any]) -> codebuild.BuildSpec:
        return codebuild.BuildSpec.from_object(mapping)

    def get_reports_build_spec_mapping(self, filename: str) -> dict[str, Any]:
        return {
            "pytest_reports": {
                "files": [filename],
                "file-format": "JUNITXML",
            }
        }


class DeployStage(Stage):
    def __init__(self, scope: Construct, construct_id: str) -> None:
        super().__init__(scope, construct_id)
        mock_glacier_stack = MockGlacierStack(self, MOCK_GLACIER_STACK_NAME)
        self.refreezer_stack = RefreezerStack(
            self, REFREEZER_STACK_NAME, mock_glacier_stack.params
        )
