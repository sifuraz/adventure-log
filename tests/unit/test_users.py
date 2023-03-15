"""Tests for handlers/test_users.py."""

from fastapi import HTTPException
import pytest

from app.db.models.users import User

from app.handlers import users as uut


test_user = User(
    id=1, username="test_user", email="test@example.com", password_hash="password_hash"
)


def test_create_user_username_already_exists(mocker):
    mocker.patch.object(uut.users, "get_user_by_username", return_value=test_user)

    with pytest.raises(HTTPException) as exception:
        uut.create_user(
            username="test_user", email="test@example.com", password="password"
        )
    assert exception.value.status_code == 409
    assert exception.value.detail == "Username already exists"


def test_create_user_email_already_exists(mocker):
    mocker.patch.object(uut.users, "get_user_by_username", return_value=None)
    mocker.patch.object(uut.users, "get_user_by_email", return_value=test_user)

    with pytest.raises(HTTPException) as exception:
        uut.create_user(
            username="new_user", email="test@example.com", password="password"
        )
    assert exception.value.status_code == 409
    assert exception.value.detail == "Email already exists"


def test_create_user(mocker):
    mocker.patch.object(uut.users, "get_user_by_username", return_value=None)
    mocker.patch.object(uut.users, "get_user_by_email", return_value=None)
    mocker.patch.object(uut.users, "create_user", return_value=test_user)

    result = uut.create_user(
        username=test_user.username, email=test_user.email, password="password"
    )
    assert result.username == test_user.username
    assert result.email == test_user.email
    assert result.password_hash == test_user.password_hash


def test_get_password_hash():
    password = "password"
    result = uut.get_password_hash(password)
    assert result != password
    assert result.startswith("$2b$")
