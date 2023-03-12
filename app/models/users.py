from ..db.config import session
from ..db.models.user import User


def create_user(username: str, email: str, password_hash: str) -> User:
    """Create a new user."""
    user = User(username=username, email=email, password_hash=password_hash)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def get_user_by_username(username: str) -> User | None:
    """Get a user by username."""
    return session.query(User).filter_by(username=username).first()


def get_user_by_email(email: str) -> User | None:
    """Get a user by email."""
    return session.query(User).filter_by(email=email).first()
