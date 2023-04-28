"""
Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
SPDX-License-Identifier: Apache-2.0
"""

import logging

logger = logging.getLogger()


class GlacierTransferModel:
    def __init__(
        self,
        primary_key: str,
        sort_key: str,
        job_id: str,
        start_timestamp: str,
        archive_id: str,
        vault_name: str,
        retrieval_type: str,
        archive_size: str,
        description: str,
        s3_bucket: str,
        s3_key: str,
    ) -> None:
        self.primary_key = primary_key
        self.sort_key = sort_key
        self.job_id = job_id
        self.start_timestamp = start_timestamp
        self.archive_id = archive_id
        self.valut_name = vault_name
        self.retieval_type = retrieval_type
        self.archive_size = archive_size
        self.description = description
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key

    @property
    def get_primary_key(self) -> str:
        return self.primary_key

    @property
    def get_sort_key(self) -> str:
        return self.sort_key
