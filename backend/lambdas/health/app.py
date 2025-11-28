import json
from datetime import datetime, timezone

def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "status": "ok",
            "timestamp": int(datetime.now(tz=timezone.utc).timestamp())
        })
    }
