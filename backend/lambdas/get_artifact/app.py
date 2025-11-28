import json
import boto3
import os
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def _build_pk(artifact_type: str, artifact_id: str) -> str:
    return f"{artifact_type}#{artifact_id}"


def lambda_handler(event, context):
    try:
        path = event.get("pathParameters") or {}
        artifact_type = path.get("artifact_type")
        artifact_id = path.get("artifact_id")

        if not artifact_type or not artifact_id:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "artifact_type and artifact_id required"})
            }

        pk = _build_pk(artifact_type, artifact_id)

        resp = table.query(
            KeyConditionExpression=Key("pk").eq(pk)
        )

        items = resp.get("Items", [])

        if not items:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "Artifact not found"})
            }

        return {
            "statusCode": 200,
            "body": json.dumps({"items": items}),
            "headers": {"Content-Type": "application/json"}
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
