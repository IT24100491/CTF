import os

from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

app = FastAPI()

API_KEY = os.getenv("API_KEY")
TEST_TABLE = os.getenv("TEST_TABLE", "test_users")

# TODO: add API authentication
# TODO: add database connection
# TODO: add user data endpoint


@app.get("/api/v1/health")
def health():
    return {"status": "ok"}
