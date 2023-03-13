import bcrypt
from fastapi import HTTPException

from ..models import users


def create_user(username: str, email: str, password: str) -> users.User:
    """Create a new user."""
    if users.get_user_by_username(username):
        raise HTTPException(
            status_code=409,
            detail="Username already exists",
        )
    if users.get_user_by_email(email):
        raise HTTPException(
            status_code=409,
            detail="Email already exists",
        )
    password_hash = get_password_hash(password)

    db_user = users.create_user(
        username=username, email=email, password_hash=password_hash
    )
    return db_user


def login_user(username: str, password: str) -> users.User:
    """Login a user."""
    if not (db_user := users.get_user_by_username(username)):
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    if not bcrypt.checkpw(
        password.encode("utf-8"), db_user.password_hash.encode("utf-8")
    ):
        raise HTTPException(
            status_code=401,
            detail="Incorrect password",
        )
    return db_user


def get_password_hash(password: str) -> str:
    """Hash a password."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
