import json
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

# Plain handler function for direct invocation
def handler(request, context):
    return {
        "statusCode": 200,
        "headers": {"content-type": "application/json"},
        "body": json.dumps({"ok": True, "service": "n8n-trends-api"})
    }

# Starlette endpoint handler
async def api_handler(request):
    return JSONResponse({"ok": True, "service": "n8n-trends-api"})

# Starlette ASGI application
asgi_app = Starlette(
    routes=[
        Route("/", api_handler, methods=["GET", "POST"]),
        Route("/api", api_handler, methods=["GET", "POST"]),
    ]
)
