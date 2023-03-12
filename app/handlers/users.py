import bcrypt
from fastapi import HTTPException

from ..models import users
from ..schemas.users import UserCreate


def create_user(user: UserCreate):
    """Create a new user."""
    if users.get_user_by_username(user.username):
        raise HTTPException(
            status_code=409,
            detail="Username already exists",
        )
    if users.get_user_by_email(user.email):
        raise HTTPException(
            status_code=409,
            detail="Email already exists",
        )
    password_hash = get_password_hash(user.password)

    db_user = users.create_user(
        username=user.username, email=user.email, password_hash=password_hash
    )
    return db_user


def get_password_hash(password: str) -> str:
    """Hash a password."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
