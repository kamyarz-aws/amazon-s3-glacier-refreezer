// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0

/**
 * @author Solution Builders
 */

const { expect, assert } = require("chai");
const sinon = require("sinon");

const parameterParser = require("../lib/parameterParser");

// (Optional) Keep test output free of error messages printed by our lambda function
sinon.stub(console, "error");

describe("-- Request Inventory Test --", () => {
    describe("-- Parameter Parser Test --", () => {
        describe("Vault name", () => {
            it("Should return FALSE if no vaultName", async () => {
                const sourceVault = null;
                const response = await parameterParser.checkRquiredParameter(sourceVault);
                expect(response).to.equal(false);
            });
            it("Should return TRUE if vaultName is supplied", async () => {
                const sourceVault = "MyTestVault";
                const response = await parameterParser.checkRquiredParameter(sourceVault);
                expect(response).to.equal(true);
            });
        });

        describe("SNS Topic", () => {
            it("Should return FALSE if no snsTopic", async () => {
                const snsTopic = null;
                const response = await parameterParser.checkRquiredParameter(snsTopic);
                expect(response).to.equal(false);
            });
            it("Should return TRUE if snsTopic is supplied", async () => {
                const snsTopic = "MySNSTopic";
                const response = await parameterParser.checkRquiredParameter(snsTopic);
                expect(response).to.equal(true);
            });
        });

        describe("stagingBucket", () => {
            it("Should return FALSE if no stagingBucket", async () => {
                const stagingBucket = null;
                const response = await parameterParser.checkRquiredParameter(stagingBucket);
                expect(response).to.equal(false);
            });
            it("Should return TRUE if stagingBucket is supplied", async () => {
                const stagingBucket = "MyDestinationBucket";
                const response = await parameterParser.checkRquiredParameter(stagingBucket);
                expect(response).to.equal(true);
            });
        });

        describe("cloudTrainExportConf === YES", () => {
            it("Should return FALSE if NULL cloudTrainExportConf", async () => {
                const cloudTrainExportConfVal = null;
                const response = await parameterParser.isValidParameter("Yes", cloudTrainExportConfVal);
                expect(response).to.equal(false);
            });
            it("Should return FALSE if cloudTrainExportConf = NO", async () => {
                const cloudTrainExportConfVal = "No";
                const response = await parameterParser.isValidParameter("Yes", cloudTrainExportConfVal);
                expect(response).to.equal(false);
            });
            it("Should return TRUE if  cloudTrainExportConf = YES", async () => {
                const cloudTrainExportConfVal = "Yes";
                const response = await parameterParser.isValidParameter("Yes", cloudTrainExportConfVal);
                expect(response).to.equal(true);
            });
        });

        describe("snsVaultConf === YES", () => {
            it("Should return FALSE if NULL snsVaultConf", async () => {
                const snsVaultConfVal = null;
                const response = await parameterParser.isValidParameter("Yes", snsVaultConfVal);
                expect(response).to.equal(false);
            });

            it("Should return FALSE if snsVaultConf = NO", async () => {
                const snsVaultConfVal = "No";
                const response = await parameterParser.isValidParameter("Yes", snsVaultConfVal);
                expect(response).to.equal(false);
            });
            it("Should return TRUE if  snsVaultConf = YES", async () => {
                const snsVaultConfVal = "Yes";
                const response = await parameterParser.isValidParameter("Yes", snsVaultConfVal);
                expect(response).to.equal(true);
            });
        });
    });
});
