from fastapi import FastAPI

app = FastAPI()

@app.get("/get_trends")
def read_root():
    return {"message": "Hello World"}
