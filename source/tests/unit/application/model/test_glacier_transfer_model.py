"""
Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
SPDX-License-Identifier: Apache-2.0
"""

import pytest
from datetime import datetime
from refreezer.application.model.glacier_transfer_model import (
    GlacierTransferModel,
)


@pytest.fixture
def glacier_transfer_model() -> GlacierTransferModel:
    return GlacierTransferModel(
        primary_key="partition_key",
        sort_key="sort_key",
        job_id="job_id",
        start_timestamp=str(datetime.now()),
        archive_id="archive_id",
        vault_name="vault_name",
        retrieval_type="retrieval_type",
        archive_size="archive_size",
        description="description",
        s3_bucket="s3_bucket",
        s3_key="s3_key",
    )


def test_glacier_transfer_model_properties(
    glacier_transfer_model: GlacierTransferModel,
) -> None:
    assert glacier_transfer_model.get_primary_key == "partition_key"
    assert glacier_transfer_model.get_sort_key == "sort_key"
