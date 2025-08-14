from fastapi import FastAPI
from fastapi.responses import JSONResponse
from mangum import Mangum

app = FastAPI(title="n8n-trends-api")

@app.get("/")
def root():
    return {"ok": True, "service": "n8n-trends-api"}

@app.get("/get_trends")
def get_trends():
    return JSONResponse({"ok": True, "data": []})

# Mangum handler for Vercel
handler = Mangum(app)
