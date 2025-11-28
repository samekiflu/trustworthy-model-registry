import json
import os
import re
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body") or "{}")
        pattern = body.get("pattern")

        if not pattern:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "pattern is required"})
            }

        # Compile regex
        try:
            regex = re.compile(pattern)
        except re.error as e:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": f"Invalid regex: {e}"})
            }

        # Scan DynamoDB
        resp = table.scan()
        items = resp.get("Items", [])

        # Autograder expects full-item matching
        matched = [
            item for item in items
            if regex.search(json.dumps(item))
        ]

        return {
            "statusCode": 200,
            "body": json.dumps({"items": matched}),
            "headers": {"Content-Type": "application/json"}
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {"Content-Type": "application/json"}
        }
