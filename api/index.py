from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok", "message": "Hello from Vercel Python FastAPI"}

@app.get("/get_trends")
def get_trends():
    return JSONResponse({"ok": True, "data": []})
