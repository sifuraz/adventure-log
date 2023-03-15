from pydantic import BaseModel

from ..db.models.adventures import AdventureTypeEnum


class AdventureCreate(BaseModel):
    name: str
    type: AdventureTypeEnum
