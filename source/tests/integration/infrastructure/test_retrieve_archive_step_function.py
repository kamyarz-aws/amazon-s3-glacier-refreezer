"""
Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
SPDX-License-Identifier: Apache-2.0
"""

import os
from typing import TYPE_CHECKING, Any
import boto3
import json
import pytest
from tests.integration.infrastructure import sfn_util
from refreezer.infrastructure.stack import OutputKeys

if TYPE_CHECKING:
    from mypy_boto3_stepfunctions import SFNClient
else:
    SFNClient = object

workflow_run_id = "workflow_run_123"


@pytest.fixture
def default_input() -> str:
    return json.dumps({"workflow_run": workflow_run_id})


@pytest.fixture(autouse=True, scope="module")
def setup() -> Any:
    sfn_util.put_inventory_files_in_s3()
    yield
    # sfn_util.delete_inventory_files_from_s3()


def test_state_machine_start_execution() -> None:
    client: SFNClient = boto3.client("stepfunctions")
    response = client.start_execution(
        stateMachineArn=os.environ[OutputKeys.RETRIEVE_ARCHIVE_STATE_MACHINE_ARN]
    )
    assert 200 == response["ResponseMetadata"]["HTTPStatusCode"]
    assert response["executionArn"] is not None


def test_state_machine_distributed_map(default_input: str) -> None:
    client: SFNClient = boto3.client("stepfunctions")
    response = client.start_execution(
        stateMachineArn=os.environ[OutputKeys.RETRIEVE_ARCHIVE_STATE_MACHINE_ARN],
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
            "Retrieve archive distributed map failed to run successfully."
        )


def test_state_machine_retrieve_archive_from_ddb(default_input: str) -> None:
    client: SFNClient = boto3.client("stepfunctions")
    response = client.start_execution(
        stateMachineArn=os.environ[OutputKeys.RETRIEVE_ARCHIVE_STATE_MACHINE_ARN],
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
