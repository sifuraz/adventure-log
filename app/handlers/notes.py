from ..models.notes import create_note


def add_note(is_secret: bool, session_id: int, text: str, user_id: int) -> None:
    """Create a note for a session."""
    create_note(text, not is_secret, user_id, session_id)
    return None
