from fastapi import APIRouter

from ..handlers import users
from ..schemas.users import UserCreate, UserLogin

router = APIRouter()


@router.post("/user", status_code=201)
async def create_user(user: UserCreate):
    users.create_user(user.username, user.email, user.password)
    return {"message": "User created successfully"}


@router.post("/user/login", status_code=200)
async def login_user(user: UserLogin):
    users.login_user(user.username, user.password)
    return {"message": "User logged in successfully"}
