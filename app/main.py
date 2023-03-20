from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from .db.models.adventures import Adventure, AdventurePlayer
from .db.models.characters import Character
from .db.models.invitations import Invitation
from .db.models.users import User
from .handlers.adventures import get_adventures_details, get_invited_adventures
from .models.users import clear_user_session, get_current_user
from .routers import adventures, characters, users
from .settings import static, templates

# TODO response schemas granularity
# TODO global dependencies
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
app.include_router(
    adventures.router,
    tags=["adventures"],
    dependencies=[Depends(get_current_user)],
)
app.include_router(
    characters.router,
    tags=["characters"],
    dependencies=[Depends(get_current_user)],
)

app.mount("/static", static, name="static")


@app.get("/")
def root(user: User = Depends(get_current_user)):
    if not user:
        return RedirectResponse(url="/login", status_code=303)

    return RedirectResponse(url="/dashboard", status_code=303)


@app.get("/login", response_class=HTMLResponse)
@app.get(
    "/logout", response_class=HTMLResponse, dependencies=[Depends(clear_user_session)]
)
def show_login(request: Request, error=None):
    response = templates.TemplateResponse(
        "login.html", {"request": request, "error": error}
    )
    response.delete_cookie(key="session_token")
    return response


@app.get("/register", response_class=HTMLResponse)
def show_register(request: Request, error=None):
    return templates.TemplateResponse(
        "register.html", {"request": request, "error": error}
    )


@app.get("/dashboard")
def dashboard(request: Request, error=None, user: User = Depends(get_current_user)):
    if not user:
        return RedirectResponse(url="/login", status_code=303)

    adventures_details = get_adventures_details(user.id)
    invited_adventures = get_invited_adventures(user.email)
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "error": error,
            "adventures": adventures_details,
            "invited_adventures": invited_adventures,
            "user": user,
        },
    )
