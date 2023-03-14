import bcrypt
import jwt

from ..settings import jwt_secret


def get_password_hash(password: str) -> str:
    """Hash a password."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def generate_session_token(username: str, password_hash: str) -> str:
    """Generate a session token."""
    payload = {"username": username, "password": password_hash}
    session_token = jwt.encode(payload, jwt_secret, algorithm="HS256")
    return session_token
