import os

from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException

load_dotenv()

app = FastAPI()

API_KEY = os.getenv("API_KEY")
TEST_TABLE = os.getenv("TEST_TABLE", "test_users")


@app.get("/api/v1/health")
def health():
    return {"status": "ok"}


@app.get("/api/v1/data")
def get_data(x_api_key: str = Header(default="")):

    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    # TODO: add database connection
    # TODO: fetch data from TEST_TABLE

    return {"status": "ok"}
