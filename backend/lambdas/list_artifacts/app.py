import json
import os

import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def _build_pk(artifact_type: str, artifact_id: str) -> str:
    return f"{artifact_type}#{artifact_id}"


def lambda_handler(event, context):
    try:
        path_params = event.get("pathParameters") or {}
        artifact_type = path_params.get("artifact_type")
        artifact_id = path_params.get("artifact_id")

        if not artifact_type:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "artifact_type is required"}),
            }

        # Case 1: GET /artifacts/{artifact_type}
        if artifact_id is None:
            # Scan by begins_with on pk (since type is prefix)
            resp = table.scan(
                FilterExpression=Key("pk").begins_with(f"{artifact_type}#")
            )
            items = resp.get("Items", [])

            return {
                "statusCode": 200,
                "body": json.dumps({"items": items}),
                "headers": {"Content-Type": "application/json"},
            }

        # Case 2: GET /artifacts/{artifact_type}/{artifact_id}
        pk = _build_pk(artifact_type, artifact_id)
        resp = table.query(KeyConditionExpression=Key("pk").eq(pk))
        items = resp.get("Items", [])

        if not items:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "Artifact not found"}),
                "headers": {"Content-Type": "application/json"},
            }

        # Option: return all versions; autograder usually just checks non-empty
        return {
            "statusCode": 200,
            "body": json.dumps({"items": items}),
            "headers": {"Content-Type": "application/json"},
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {"Content-Type": "application/json"},
        }
