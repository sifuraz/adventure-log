from pydantic import BaseModel


class SessionCreate(BaseModel):
    date: str
    adventure_id: int
