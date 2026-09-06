from fastapi import FastAPI

app = FastAPI()

# TODO: add API authentication
# TODO: add database connection
# TODO: add user data endpoint


@app.get("/api/v1/health")
def health():
    return {"status": "ok"}
