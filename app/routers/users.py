from fastapi import APIRouter

from ..handlers import users
from ..schemas.users import UserCreate

router = APIRouter()


@router.post("/user", status_code=201)
async def create_user(user: UserCreate):
    users.create_user(user.username, user.email, user.password)
    return {"message": "User created successfully"}
