from pydantic import BaseModel

from ..db.models.adventures import AdventureTypeEnum


class AdventureCreate(BaseModel):
    name: str
    type: AdventureTypeEnum


class AdventureInvite(BaseModel):
    email: str
    adventure_id: int


class AdventureId(BaseModel):
    adventure_id: int
