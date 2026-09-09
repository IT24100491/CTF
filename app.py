import os
import sqlite3

from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException

load_dotenv()

app = FastAPI()

API_KEY = os.getenv("API_KEY")
USERNAME = os.getenv("USERNAME")
SECRET_KEY = os.getenv("SECRET_KEY")
TEST_TABLE = os.getenv("TEST_TABLE", "test_users")
FLAG = os.getenv("FLAG")


@app.get("/api/v1/health")
def health():
    return {"status": "ok"}


@app.get("/api/v1/data")
def get_data(x_api_key: str = Header(default="")):

    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    connection = sqlite3.connect("staging.db")
    connection.row_factory = sqlite3.Row

    # TODO: fetch data from TEST_TABLE

    connection.close()

    return {"status": "ok"}


@app.get("/api/v1/info")
def info():
    return {"service": "user-service", "environment": "staging", "version": "1.2.0"}


@app.get("/api/v1/users")
def get_user(user_id: int):
    # TODO: fetch user by ID

    return {"id": user_id, "status": "not implemented"}
