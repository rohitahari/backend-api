from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {
        "message": "Backend running",
        "environment": "production",
        "debug": False
    }
