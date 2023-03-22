from pydantic import BaseModel


class NoteCreate(BaseModel):
    is_secret: bool
    session_id: int
    text: str
