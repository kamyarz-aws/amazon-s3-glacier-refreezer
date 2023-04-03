"""
Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
SPDX-License-Identifier: Apache-2.0
"""

from typing import TYPE_CHECKING, Any
from datetime import datetime, timedelta
from refreezer.infrastructure.stack import OutputKeys

import random
import string
import boto3
import time
import hashlib
import binascii
import csv
import io
import os

if TYPE_CHECKING:
    from mypy_boto3_stepfunctions import SFNClient
    from mypy_boto3_s3 import S3Client

else:
    SFNClient = object
    S3Client = object


workflow_run_id = "workflow_run_123"


def get_state_machine_output(executionArn: str, timeout: int) -> str:
    client: SFNClient = boto3.client("stepfunctions")
    start_time = time.time()
    sf_output: str = "TIMEOUT EXCEEDED"
    while (time.time() - start_time) < timeout:
        time.sleep(1)
        sf_describe_response = client.describe_execution(executionArn=executionArn)
        status = sf_describe_response["status"]
        if status == "RUNNING":
            continue
        elif status == "SUCCEEDED":
            sf_output = sf_describe_response["output"]
            break
        else:
            # for status: FAILED, TIMED_OUT or ABORTED
            raise Exception(f"Execution {status}")

    return sf_output


def wait_till_state_machine_finish(executionArn: str, timeout: int) -> None:
    client: SFNClient = boto3.client("stepfunctions")
    start_time = time.time()
    while (time.time() - start_time) < timeout:
        time.sleep(1)
        sf_describe_response = client.describe_execution(executionArn=executionArn)
        status = sf_describe_response["status"]
        if status == "RUNNING":
            continue
        break


def put_inventory_files_in_s3() -> Any:
    client: S3Client = boto3.client("s3")
    num_inventory_files = 2
    num_archives = 5
    archives_size_in_mb = 5
    file_name_prefix = f"{workflow_run_id}/sorted_inventory/test_inventory"
    for n in range(num_inventory_files):
        csv_buffer = generate_inventory_file(num_archives, archives_size_in_mb)
        client.put_object(
            Bucket=os.environ[OutputKeys.INVENTORY_BUCKET_NAME],
            Key=f"{file_name_prefix}_{n}.csv",
            Body=csv_buffer.getvalue().encode("utf-8"),
        )


def delete_inventory_files_from_s3() -> Any:
    client: S3Client = boto3.client("s3")
    file_name_prefix = f"{workflow_run_id}/test_inventory"
    inventories_keys = [f"{file_name_prefix}_{n}.csv" for n in range(5)]
    client.delete_objects(
        Bucket=os.environ[OutputKeys.INVENTORY_BUCKET_NAME],
        Delete={"Objects": [{"Key": key} for key in inventories_keys]},
    )


def generate_inventory_file(num_archives: int, archives_size_in_mb: int) -> io.StringIO:
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 1, 1)

    archives_list = [
        [
            "".join(random.choices(string.ascii_letters + string.digits, k=138)),
            "Archive Description "
            + "".join(random.choices(string.ascii_letters + string.digits, k=130)),
            (
                start_date
                + timedelta(
                    seconds=random.randint(
                        0, int((end_date - start_date).total_seconds())
                    )
                )
            ).strftime("%Y-%m-%dT%H:%M:%SZ"),
            archives_size_in_mb,
            binascii.hexlify(
                hashlib.sha256(os.urandom(2**20 * archives_size_in_mb)).digest()
            ).decode("utf-8"),
        ]
        for _ in range(num_archives)
    ]

    csv_buffer = io.StringIO()
    writer = csv.writer(
        csv_buffer,
        quoting=csv.QUOTE_MINIMAL,
        lineterminator="\n",
        escapechar="\\",
        doublequote=False,
    )
    writer.writerow(
        [
            "ArchiveId",
            "ArchiveDescription",
            "CreationDate",
            "Size",
            "SHA256TreeHash",
        ]
    )
    writer.writerows(archives_list)

    return csv_buffer
