from pathlib import Path

from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .db.models.users import User
from .models.users import get_current_user
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
app.mount(
    "/static", StaticFiles(directory=str(Path(BASE_DIR, "static"))), name="static"
)
templates = Jinja2Templates(directory=str(Path(BASE_DIR, "templates")))


@app.get("/")
def root(user: User = Depends(get_current_user)):
    if not user:
        return RedirectResponse(url="/login", status_code=303)

    return RedirectResponse(url="/dashboard", status_code=303)


@app.get("/login", response_class=HTMLResponse)
async def show_login(request: Request, error=None):
    return templates.TemplateResponse(
        "login.html", {"request": request, "error": error}
    )


@app.get("/register", response_class=HTMLResponse)
async def show_register(request: Request, error=None):
    return templates.TemplateResponse(
        "register.html", {"request": request, "error": error}
    )


@app.get("/dashboard")
def dashboard(request: Request, error=None, user: User = Depends(get_current_user)):
    if not user:
        return RedirectResponse(url="/login", status_code=303)

    return templates.TemplateResponse(
        "dashboard.html", {"request": request, "error": error}
    )
