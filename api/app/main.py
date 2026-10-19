import os

import jwt
from cryptography.fernet import Fernet
from fastapi import FastAPI, Header, HTTPException

from . import portal

app = FastAPI(
    title="Account Management API",
    version="1.0.1",
)

app.include_router(portal.router)

JWT_SECRET = os.getenv("JWT_SECRET", "Ver1d1an_Analyt1cs_JWT_S3cr3t_K3y_2024")
JWT_ALGORITHM = "HS256"

FERNET_KEY = os.getenv("FERNET_KEY", "MKmfEgnGra5Bor7ZG8BkNpYp9xID5_skwfQAksrnzf0=")
fernet = Fernet(FERNET_KEY)

FLAG = "PT{st4g1ng_1s_pr0ductn_r0le_tru5t_bug}"

USERS = [
    {
        "id": 1,
        "username": "a.silva",
        "role": "support",
        "department": "Customer Success",
    },
    {
        "id": 2,
        "username": "r.perera",
        "role": "engineer",
        "department": "Platform Engineering",
    },
    {
        "id": 3,
        "username": "n.fernando",
        "role": "it_admin",
        "department": "IT Operations",
    },
    {
        "id": 4,
        "username": "flag",
        "role": FLAG,
        "department": "Flag Department",
    },
]


def encrypt_field(value: str) -> str:
    return fernet.encrypt(value.encode()).decode()


@app.get("/api/v1/health")
def health():
    return {"status": "ok"}


@app.get("/api/v1/users")
def get_users(authorization: str = Header(default="")):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")

    token = authorization.removeprefix("Bearer ").strip()

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    if payload.get("role") != "admin":
        raise HTTPException(
            status_code=403,
            detail=f"Role '{payload.get('role')}' is not authorized for this resource",
        )

    users = [
        {
            "id": user["id"],
            "username": encrypt_field(user["username"]),
            "role": encrypt_field(user["role"]),
            "department": encrypt_field(user["department"]),
        }
        for user in USERS
    ]

    return {
        "status": "ok",
        "users": users,
    }
