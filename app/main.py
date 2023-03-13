from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .routers import users

# TODO response schemas granularity
app = FastAPI()
app.include_router(
    users.router,
    tags=["users"],
    responses={
        401: {"description": "Incorrect password"},
        404: {"description": "User not found"},
        409: {"description": "User already exists"},
    },
)

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(Path(BASE_DIR, "templates")))


@app.get("/login", response_class=HTMLResponse)
async def show_login(request: Request, error=None):
    return templates.TemplateResponse(
        "login.html", {"request": request, "error": error}
    )
