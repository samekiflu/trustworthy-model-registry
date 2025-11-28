Trustworthy Model Registry — Phase 2
ECE 461 / 30861 — Software Engineering

This repository contains my full implementation of Phase 2: Trustworthy Model Registry, a serverless backend system deployed on AWS. The goal of this project is to design and implement a reliable, transparent, and auditable registry for machine learning artifacts such as models, datasets, and code resources.

Phase 2 extends earlier work by adding persistent storage, scalable APIs, and several essential operations that allow artifacts to be registered, queried, listed, searched, and reset. All endpoints conform to the OpenAPI specification provided by the course, and the deployment is handled through AWS SAM, API Gateway (HTTP API), Lambda, and DynamoDB.

🚀 Project Overview

A trustworthy model registry is essential for tracking machine learning assets, their versions, metadata, and provenance.
This backend service:

Stores artifacts in a DynamoDB table using a pk/sk schema

Exposes a REST API for interacting with the registry

Provides consistent methods to register, retrieve, search, and reset artifacts

Implements a serverless architecture suitable for scaling and low operational cost

Follows the course-provided OpenAPI spec exactly, ensuring autograder compatibility

This implementation focuses solely on the backend; the frontend/UI is optional and can be added later.

🔧 Core Features (Implemented)
✔️ Health Check

Verifies that the backend is deployed and reachable.

✔️ Register an Artifact (POST /artifacts)

Stores a new artifact with:

type (model/dataset/code)

artifact_id

version

metadata (optional)

automatic timestamps
Writes to DynamoDB using a composite key:
pk = type#id, sk = v#version

✔️ Get a Specific Artifact (GET /artifacts/{artifact_type}/{artifact_id})

Returns all versions of a specific artifact.

✔️ List Artifacts (GET /artifacts/{artifact_type})

Returns all artifacts of a given type (e.g., all models).

✔️ List Specific Artifact + Version (GET /artifacts/{artifact_type}/{artifact_id})

Handles both:

list all versions

get specific artifact/version
depending on request

✔️ Regex Search (POST /artifact/byRegEx)

Performs a regex match on artifact IDs to support flexible retrieval.

✔️ Reset Registry (POST /reset)

Deletes all stored records from DynamoDB — useful for testing and autograder resets.

🏗️ Architecture Summary

The backend is deployed using:

AWS Lambda for all compute

AWS API Gateway (HTTP API) for routing requests

AWS DynamoDB (pay-per-request mode) for storing artifacts

AWS SAM for infrastructure-as-code

Each API endpoint maps to a dedicated Lambda function under
backend/lambdas/.

📄 OpenAPI Specification

The full API contract is defined by the course staff and included under:

openapi/ece461_fall_2025_openapi_spec.yaml

All endpoints and request/response shapes follow this specification precisely to ensure autograder compliance.

🧪 Testing & Autograder

The implementation has been fully deployed and tested using:

curl commands

DynamoDB verification

Full local and remote endpoint validation

All required operations work end-to-end and are ready for submission to the ECE 461 / 30861 Autograder (Phase 2) via GitHub authentication.
