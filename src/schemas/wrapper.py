from typing import List

from pydantic import BaseModel

from src.schemas.bet import BetSchema
from src.schemas.event import EventSchema


class BaseWrapper(BaseModel):
    status: int = 200
    error: bool = False


class BetListWrapper(BaseWrapper):
    payload: List[BetSchema]


class EventListWrapper(BaseWrapper):
    payload: List[EventSchema]


class BaseErrorWrapper(BaseWrapper):
    status: int = 400
    error: bool = True
    reason: str
