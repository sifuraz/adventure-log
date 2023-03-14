from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from ..handlers import users
from ..schemas.users import UserCreate, UserLogin

router = APIRouter()


@router.post("/user", status_code=201)
async def create_user(user: UserCreate):
    session_token = users.create_user(user.username, user.email, user.password)
    response = RedirectResponse(url="/dashboard", status_code=303)
    response.set_cookie(key="session_token", value=session_token)
    return response


@router.post("/user/login", status_code=200)
async def login_user(user: UserLogin):
    session_token = users.login_user(user.username, user.password)
    response = RedirectResponse(url="/dashboard", status_code=303)
    response.set_cookie(key="session_token", value=session_token)
    return response
