import bcrypt
from fastapi import HTTPException

from ..models import users
from ..utils import security


def create_user(username: str, email: str, password: str) -> str:
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
    password_hash = security.get_password_hash(password)

    db_user = users.create_user(
        username=username, email=email, password_hash=password_hash
    )
    session_token = security.generate_session_token(
        db_user.username, db_user.password_hash
    )
    users.store_user_session(session_token, db_user.id)
    return session_token


def login_user(username: str, password: str) -> str:
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
    session_token = security.generate_session_token(
        db_user.username, db_user.password_hash
    )
    users.store_user_session(session_token, db_user.id)
    return session_token
