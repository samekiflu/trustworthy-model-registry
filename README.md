# Trustworthy Model Registry (Phase 2)

This repository contains a deployment-ready skeleton for the Phase 2
"Trustworthy Model Registry" project. It is structured to run on AWS Lambda
with DynamoDB and S3 as backing services and is intended to be wired to the
provided OpenAPI specification (`openapi/ece461_fall_2025_openapi_spec.yaml`).

## Layout

- `backend/core/` — metric engine and handlers reused from Phase 1.
- `backend/registry/` — new registry and rating services for Phase 2.
- `backend/lambdas/` — AWS Lambda handlers that back the REST API.
- `openapi/` — OpenAPI spec provided by the course staff.
- `infrastructure/` — AWS SAM template skeleton to deploy the stack.

## Environment variables

The Lambda functions expect the following environment variables:

- `ARTIFACT_TABLE_NAME` — name of the DynamoDB table for artifact metadata.
- `ARTIFACT_BUCKET_NAME` — name of the S3 bucket for artifact files.

## Notes

- The rating service currently returns synthetic values for some metrics and
  should be extended to call `ModelEvaluator` from `backend/core` to compute
  real scores from HuggingFace / GitHub URLs stored in the artifact metadata.
- The SAM template is a skeleton and must be extended to wire each Lambda
  handler to the correct API Gateway routes defined in the OpenAPI spec.
