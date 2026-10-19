import secrets
from pathlib import Path

from fastapi import APIRouter, Cookie, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, RedirectResponse

from .mongo_mock import find_one, matches

router = APIRouter()

STATIC_DIR = Path(__file__).parent / "static_files" / "portal"

USERS = [
    {
        "username": "n.fernando",
        "password": "Qx7!mPz2Lw9#Rk4T",
        "display_name": "N. Fernando",
    },
]

SESSIONS: dict[str, str] = {}

FILES = ["notes.txt", "handbook.txt", "flag.txt", "not-a-secret.jpg"]

LOGIN_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<title>Login Portal</title>
<style>
  body { font-family: Arial, Helvetica, sans-serif; background: #eef1f4; margin: 0;
         display: flex; align-items: center; justify-content: center; height: 100vh; }
  .card { background: #fff; border: 1px solid #d7dce1; border-radius: 6px; padding: 32px 36px;
          width: 320px; box-shadow: 0 1px 4px rgba(0,0,0,0.08); }
  h1 { font-size: 18px; margin: 0 0 4px; color: #222; }
  p.sub { font-size: 12px; color: #777; margin: 0 0 20px; }
  label { display: block; font-size: 12px; color: #444; margin-bottom: 4px; }
  input { width: 100%; padding: 8px; margin-bottom: 14px; border: 1px solid #ccd2d8;
          border-radius: 4px; box-sizing: border-box; font-size: 13px; }
  button { width: 100%; padding: 9px; background: #2c5aa0; color: #fff; border: none;
           border-radius: 4px; font-size: 13px; cursor: pointer; }
  button:hover { background: #244c87; }
  #error { color: #b3261e; font-size: 12px; margin-top: 12px; display: none; }
</style>
</head>
<body>
  <div class="card">
    <h1>Login Portal</h1>
    <p class="sub">Veridian Analytics, internal use only</p>
    <form id="loginForm" novalidate>
      <label for="username">Username</label>
      <input id="username" name="username" type="text" autocomplete="username" required minlength="1" />
      <label for="password">Password</label>
      <input id="password" name="password" type="password" autocomplete="current-password" required minlength="1" />
      <button type="submit">Sign in</button>
    </form>
    <div id="error"></div>
  </div>
  <script>
    document.getElementById("loginForm").addEventListener("submit", async (e) => {
      e.preventDefault();
      const usernameEl = document.getElementById("username");
      const passwordEl = document.getElementById("password");
      const username = usernameEl.value.trim();
      const password = passwordEl.value;
      const errEl = document.getElementById("error");

      if (!username || !password) {
        errEl.textContent = "Username and password are required.";
        errEl.style.display = "block";
        return;
      }
      errEl.style.display = "none";

      const res = await fetch("/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });
      if (res.ok) {
        window.location.href = "/files";
      } else {
        const data = await res.json();
        errEl.textContent = data.detail || "Login failed.";
        errEl.style.display = "block";
      }
    });
  </script>
</body>
</html>
"""

FILES_PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<title>Login Portal, Files</title>
<style>
  body {{ font-family: Arial, Helvetica, sans-serif; background: #eef1f4; margin: 0; padding: 40px; }}
  .card {{ background: #fff; border: 1px solid #d7dce1; border-radius: 6px; padding: 28px 32px;
          max-width: 480px; margin: 0 auto; box-shadow: 0 1px 4px rgba(0,0,0,0.08); }}
  h1 {{ font-size: 18px; margin: 0 0 4px; color: #222; }}
  p.sub {{ font-size: 12px; color: #777; margin: 0 0 20px; }}
  ul {{ list-style: none; padding: 0; margin: 0; }}
  li {{ padding: 10px 0; border-bottom: 1px solid #eee; font-size: 13px; }}
  li:last-child {{ border-bottom: none; }}
  a {{ color: #2c5aa0; text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  .logout {{ font-size: 12px; margin-top: 20px; display: inline-block; color: #888; }}
</style>
</head>
<body>
  <div class="card">
    <h1>Welcome, {display_name}</h1>
    <p class="sub">Staging file area</p>
    <ul>
      {file_items}
    </ul>
    <a class="logout" href="/logout">Sign out</a>
  </div>
</body>
</html>
"""


@router.get("/", response_class=HTMLResponse)
def login_page(session: str | None = Cookie(default=None)):
    if session in SESSIONS:
        return RedirectResponse(url="/files")
    return LOGIN_PAGE


@router.post("/login")
async def login(request: Request):
    body = await request.json()
    username = body.get("username")
    password = body.get("password")

    user = find_one(USERS, {"username": username})
    if user is None:
        return JSONResponse(status_code=401, content={"detail": "User not found"})

    if not matches(user["password"], password):
        return JSONResponse(status_code=401, content={"detail": "Invalid password"})

    token = secrets.token_urlsafe(24)
    SESSIONS[token] = user["username"]

    response = JSONResponse({"status": "ok"})
    response.set_cookie("session", token, httponly=True)
    return response


@router.get("/logout")
def logout(session: str | None = Cookie(default=None)):
    if session:
        SESSIONS.pop(session, None)
    response = RedirectResponse(url="/")
    response.delete_cookie("session")
    return response


@router.get("/files", response_class=HTMLResponse)
def list_files(session: str | None = Cookie(default=None)):
    username = SESSIONS.get(session) if session else None
    if username is None:
        return RedirectResponse(url="/")

    user = find_one(USERS, {"username": username})
    file_items = "\n".join(
        f'<li><a href="/files/{name}">{name}</a></li>' for name in FILES
    )
    return FILES_PAGE_TEMPLATE.format(
        display_name=user["display_name"] if user else username,
        file_items=file_items,
    )


@router.get("/files/{filename}")
def download_file(filename: str, session: str | None = Cookie(default=None)):
    if session not in SESSIONS:
        return RedirectResponse(url="/")

    if filename not in FILES:
        return JSONResponse(status_code=404, content={"detail": "Not found"})

    return FileResponse(STATIC_DIR / filename)
