from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from src.utils.enums import EventState


class IDBetSchema(BaseModel):
    id: int


class CreateBetSchema(BaseModel):
    amount: Decimal = Field(decimal_places=2, gt=0)
    event_id: int


class BetSchema(IDBetSchema, CreateBetSchema):
    state: EventState

    model_config = ConfigDict(from_attributes=True)
