"""Tests for models/test_users.py."""
from app.db.models.user import User

from app.models import users as uut


def test_create_user(session):
    """Test creating a new user."""
    # TODO: Figure out how to mock the session
    print("Creating user")
    user = uut.create_user("testuser2", "test2@example.com", "password")

    assert user.username == "testuser2"
    assert user.email == "test2@example.com"
    assert user.password_hash == "password"
    assert (
        session.query(User).filter(User.username == "testuser").one_or_none()
        is not None
    )


def test_get_user_by_username():
    """Test getting a user by username."""
    ...


def test_get_user_by_email():
    """Test getting a user by email."""
    ...
