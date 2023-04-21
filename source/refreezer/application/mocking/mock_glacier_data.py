"""
Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
SPDX-License-Identifier: Apache-2.0
"""
# This file is auto-generated by mock_glacier_generator.py and formatted with black
MOCK_DATA = {
    "test_mock_glacier_apis_vault": {
        "initiate-job": {
            "inventory-retrieval": {
                "ResponseMetadata": {"HTTPStatusCode": 202, "RetryAttempts": 0},
                "location": "//vaults/test_mock_glacier_apis_vault/jobs/IEQH524YNG5BY1A2ROGUBBB8AYN1B7O259OWOO3SB09GLSHV616MTS56ZC4PZ0LX9XF26GK7ZX5B4CTZKK6OAM89OZ6W",
                "jobId": "IEQH524YNG5BY1A2ROGUBBB8AYN1B7O259OWOO3SB09GLSHV616MTS56ZC4PZ0LX9XF26GK7ZX5B4CTZKK6OAM89OZ6W",
            },
            "archive-retrieval:cf2e306ff9a72790b152fb4af93a1a1d": {
                "ResponseMetadata": {"HTTPStatusCode": 202, "RetryAttempts": 0},
                "location": "//vaults/test_mock_glacier_apis_vault/jobs/W3R9AY6I79N1D4X9M605W0WA88V3BOL9LF9QCEFB2ARPRHLWSEKKQ7KRS3U54HBTYV0MQGQ6N1BOBZJCK2618O72O7BZ",
                "jobId": "W3R9AY6I79N1D4X9M605W0WA88V3BOL9LF9QCEFB2ARPRHLWSEKKQ7KRS3U54HBTYV0MQGQ6N1BOBZJCK2618O72O7BZ",
            },
        },
        "get-job-output": {
            "IEQH524YNG5BY1A2ROGUBBB8AYN1B7O259OWOO3SB09GLSHV616MTS56ZC4PZ0LX9XF26GK7ZX5B4CTZKK6OAM89OZ6W": {
                "ResponseMetadata": {"HTTPStatusCode": 200, "RetryAttempts": 0},
                "status": 200,
                "contentType": "application/json",
                "body": "ArchiveId,ArchiveDescription,CreationDate,Size,SHA256TreeHash\r\ncf2e306ff9a72790b152fb4af93a1a1d,test.txt,2023-04-24T14:07:34.000Z,8,b9f9644670e5fcd37a4c54a478d636fc37c41282d161e3e50cb3fb962aa04285\r\n",
            },
            "W3R9AY6I79N1D4X9M605W0WA88V3BOL9LF9QCEFB2ARPRHLWSEKKQ7KRS3U54HBTYV0MQGQ6N1BOBZJCK2618O72O7BZ": {
                "bytes=0-2": {
                    "ResponseMetadata": {"HTTPStatusCode": 200, "RetryAttempts": 0},
                    "status": 200,
                    "contentType": "application/octet-stream",
                    "body": "TES",
                },
                "bytes=3-5": {
                    "ResponseMetadata": {"HTTPStatusCode": 200, "RetryAttempts": 0},
                    "status": 200,
                    "contentType": "application/octet-stream",
                    "body": "TBO",
                },
                "bytes=6-8": {
                    "ResponseMetadata": {"HTTPStatusCode": 200, "RetryAttempts": 0},
                    "status": 200,
                    "contentType": "application/octet-stream",
                    "body": "DY",
                },
            },
        },
    },
    "test_vault_generation_vault": {
        "initiate-job": {
            "inventory-retrieval": {
                "ResponseMetadata": {"HTTPStatusCode": 202, "RetryAttempts": 0},
                "location": "//vaults/test_vault_generation_vault/jobs/IEQH524YNG5BY1A2ROGUBBB8AYN1B7O259OWOO3SB09GLSHV616MTS56ZC4PZ0LX9XF26GK7ZX5B4CTZKK6OAM89OZ6W",
                "jobId": "IEQH524YNG5BY1A2ROGUBBB8AYN1B7O259OWOO3SB09GLSHV616MTS56ZC4PZ0LX9XF26GK7ZX5B4CTZKK6OAM89OZ6W",
            },
            "archive-retrieval:cf2e306ff9a72790b152fb4af93a1a1d": {
                "ResponseMetadata": {"HTTPStatusCode": 202, "RetryAttempts": 0},
                "location": "//vaults/test_vault_generation_vault/jobs/W3R9AY6I79N1D4X9M605W0WA88V3BOL9LF9QCEFB2ARPRHLWSEKKQ7KRS3U54HBTYV0MQGQ6N1BOBZJCK2618O72O7BZ",
                "jobId": "W3R9AY6I79N1D4X9M605W0WA88V3BOL9LF9QCEFB2ARPRHLWSEKKQ7KRS3U54HBTYV0MQGQ6N1BOBZJCK2618O72O7BZ",
            },
            "archive-retrieval:de1cf0c183248e153ec9a57c2062073b": {
                "ResponseMetadata": {"HTTPStatusCode": 202, "RetryAttempts": 0},
                "location": "//vaults/test_vault_generation_vault/jobs/U1DTINDTEETTK0QIA9CN3K6CYMWGN1M5GYS65BUZSBKMUIV1NRGY9W858PECFIKK8NRV6QXVVHSP5I9GUC0EYJIVHYE9",
                "jobId": "U1DTINDTEETTK0QIA9CN3K6CYMWGN1M5GYS65BUZSBKMUIV1NRGY9W858PECFIKK8NRV6QXVVHSP5I9GUC0EYJIVHYE9",
            },
        },
        "get-job-output": {
            "IEQH524YNG5BY1A2ROGUBBB8AYN1B7O259OWOO3SB09GLSHV616MTS56ZC4PZ0LX9XF26GK7ZX5B4CTZKK6OAM89OZ6W": {
                "ResponseMetadata": {"HTTPStatusCode": 200, "RetryAttempts": 0},
                "status": 200,
                "contentType": "application/json",
                "body": 'ArchiveId,ArchiveDescription,CreationDate,Size,SHA256TreeHash\r\ncf2e306ff9a72790b152fb4af93a1a1d,test.txt,2023-04-24T14:07:34.000Z,8,b9f9644670e5fcd37a4c54a478d636fc37c41282d161e3e50cb3fb962aa04285\r\nde1cf0c183248e153ec9a57c2062073b,"my archive description,1""2",2023-04-24T14:07:34.000Z,9,4bea3f70ca51a975d37798a63ae730535b79431d14577d7db01691b801d5b9ce\r\n',
            },
            "W3R9AY6I79N1D4X9M605W0WA88V3BOL9LF9QCEFB2ARPRHLWSEKKQ7KRS3U54HBTYV0MQGQ6N1BOBZJCK2618O72O7BZ": {
                "bytes=0-2": {
                    "ResponseMetadata": {"HTTPStatusCode": 200, "RetryAttempts": 0},
                    "status": 200,
                    "contentType": "application/octet-stream",
                    "body": "TES",
                },
                "bytes=3-5": {
                    "ResponseMetadata": {"HTTPStatusCode": 200, "RetryAttempts": 0},
                    "status": 200,
                    "contentType": "application/octet-stream",
                    "body": "TBO",
                },
                "bytes=6-8": {
                    "ResponseMetadata": {"HTTPStatusCode": 200, "RetryAttempts": 0},
                    "status": 200,
                    "contentType": "application/octet-stream",
                    "body": "DY",
                },
            },
            "U1DTINDTEETTK0QIA9CN3K6CYMWGN1M5GYS65BUZSBKMUIV1NRGY9W858PECFIKK8NRV6QXVVHSP5I9GUC0EYJIVHYE9": {
                "ResponseMetadata": {"HTTPStatusCode": 200, "RetryAttempts": 0},
                "status": 200,
                "contentType": "application/octet-stream",
                "body": "TESTBODY2",
            },
        },
    },
}
