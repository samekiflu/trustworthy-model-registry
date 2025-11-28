import json
import os
from datetime import datetime, timezone

import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])  # FIXED


def _build_pk(artifact_type: str, artifact_id: str) -> str:
    return f"{artifact_type}#{artifact_id}"


def _build_sk(version: str) -> str:
    return f"v#{version}"


def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body") or "{}")

        artifact_type = body.get("artifact_type")
        artifact_id = body.get("artifact_id")
        version = body.get("version")
        metadata = body.get("metadata", {})

        if not artifact_type or not artifact_id or not version:
            return {
                "statusCode": 400,
                "body": json.dumps(
                    {
                        "error": "artifact_type, artifact_id, and version are required"
                    }
                ),
            }

        item = {
            "pk": _build_pk(artifact_type, artifact_id),
            "sk": _build_sk(version),
            "artifact_type": artifact_type,
            "artifact_id": artifact_id,
            "version": version,
            "metadata": metadata,
            "created_at": datetime.now(tz=timezone.utc).isoformat(),
        }

        table.put_item(Item=item)

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Artifact registered", "item": item}),
            "headers": {"Content-Type": "application/json"},
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {"Content-Type": "application/json"},
        }
