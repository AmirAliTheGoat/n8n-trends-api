import json

def handler(request, context):
    return {
        "statusCode": 200,
        "headers": {"content-type": "application/json"},
        "body": json.dumps({"ok": True, "service": "n8n-trends-api"})
    }
