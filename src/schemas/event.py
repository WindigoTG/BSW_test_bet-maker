import decimal

from pydantic import BaseModel, ConfigDict

from src.utils.enums import EventState


class EventSchema(BaseModel):
    id: int
    coefficient: decimal.Decimal
    deadline: int
    state: EventState

    model_config = ConfigDict(from_attributes=True)
