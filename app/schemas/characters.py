from pydantic import BaseModel


class CharacterCreate(BaseModel):
    name: str
    adventure_id: int
