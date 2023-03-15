from fastapi import Cookie

from ..db.config import database, redis
from ..db.models.users import User


def create_user(username: str, email: str, password_hash: str) -> User:
    """Create a new user."""
    user = User(username=username, email=email, password_hash=password_hash)
    database.add(user)
    database.commit()
    database.refresh(user)
    return user


def get_user_by_id(user_id: int) -> User | None:
    """Get a user by id."""
    return database.query(User).get(user_id)


def get_user_by_username(username: str) -> User | None:
    """Get a user by username."""
    return database.query(User).filter_by(username=username).first()


def get_user_by_email(email: str) -> User | None:
    """Get a user by email."""
    return database.query(User).filter_by(email=email).first()


def store_user_session(session_token: str, user_id: int):
    """Store the session token."""
    redis.setex(session_token, 3600, user_id)


def get_current_user(session_token: str | None = Cookie(None)) -> User | None:
    """Get the current user from the session token."""
    if not session_token:
        return None

    user_id = redis.get(session_token)
    if not user_id:
        return None

    user = get_user_by_id(int(user_id))
    return user
