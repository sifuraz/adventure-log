from ..db.config import database
from ..db.models.notes import Note


def create_note(text: str, is_public: bool, author_id: int, session_id: int) -> Note:
    """Create a note."""
    note = Note(
        text=text, is_public=is_public, author_id=author_id, session_id=session_id
    )
    database.add(note)
    database.commit()
    database.refresh(note)
    return note
