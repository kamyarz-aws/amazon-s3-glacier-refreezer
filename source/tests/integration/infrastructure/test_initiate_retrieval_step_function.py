"""
Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
SPDX-License-Identifier: Apache-2.0
"""

import os
from typing import TYPE_CHECKING, Any
import boto3
import pytest
import json

from tests.integration.infrastructure import sfn_util
from refreezer.infrastructure.stack import OutputKeys


if TYPE_CHECKING:
    from mypy_boto3_stepfunctions import SFNClient
    from mypy_boto3_dynamodb import DynamoDBClient
    from mypy_boto3_s3 import S3Client
else:
    SFNClient = object
    DynamoDBClient = object
    S3Client = object


workflow_run_id = "workflow_run_123"


@pytest.fixture
def default_input() -> str:
    return json.dumps({"workflow_run": workflow_run_id})


@pytest.fixture(autouse=True, scope="module")
def setup() -> Any:
    sfn_util.put_inventory_files_in_s3()
    yield
    # sfn_util.delete_inventory_files_from_s3()


def test_state_machine_start_execution(default_input: str) -> None:
    client: SFNClient = boto3.client("stepfunctions")
    response = client.start_execution(
        stateMachineArn=os.environ[OutputKeys.INITIATE_RETRIEVAL_STATE_MACHINE_ARN],
        input=default_input,
    )
    assert 200 == response["ResponseMetadata"]["HTTPStatusCode"]
    assert response["executionArn"] is not None

    sf_history_output = client.get_execution_history(
        executionArn=response["executionArn"], maxResults=1000
    )

    event_details = [
        event["taskSucceededEventDetails"]
        for event in sf_history_output["events"]
        if "taskSucceededEventDetails" in event
    ]

    for detail in event_details:
        if detail["resourceType"] == "aws-sdk:dynamodb":
            state_output = json.loads(detail["output"])
            archive_id = state_output["job_result"]["ArchiveId"]

            table_name = os.environ[OutputKeys.GLACIER_RETRIEVAL_TABLE_NAME]
            db_client: DynamoDBClient = boto3.client("dynamodb")
            key = {"pk": {"S": f"IR:{archive_id}"}, "sk": {"S": "meta"}}
            item = db_client.get_item(TableName=table_name, Key=key)["Item"]
            assert item["job_id"] is not None and item["start_timestamp"] is not None
            break


def test_state_machine_nested_distributed_map(default_input: str) -> None:
    client: SFNClient = boto3.client("stepfunctions")
    response = client.start_execution(
        stateMachineArn=os.environ[OutputKeys.INITIATE_RETRIEVAL_STATE_MACHINE_ARN],
        input=default_input,
    )

    sfn_util.wait_till_state_machine_finish(response["executionArn"], timeout=60)

    sf_history_output = client.get_execution_history(
        executionArn=response["executionArn"], maxResults=1000
    )

    events = [
        event
        for event in sf_history_output["events"]
        if "MapRunSucceeded" in event["type"]
    ]

    if not events:
        raise AssertionError(
            "Initiate retrieval nested distributed map failed to run successfully."
        )
