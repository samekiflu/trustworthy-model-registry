import json
import os

import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def lambda_handler(event, context):
    try:
        # Scan all items
        resp = table.scan()
        items = resp.get("Items", [])

        with table.batch_writer() as batch:
            for item in items:
                batch.delete_item(
                    Key={"pk": item["pk"], "sk": item["sk"]}
                )

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Registry reset"}),
            "headers": {"Content-Type": "application/json"},
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {"Content-Type": "application/json"},
        }
