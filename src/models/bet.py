from sqlalchemy import DECIMAL, Enum
from sqlalchemy.orm import Mapped, mapped_column

from src.models.custom_types.custom_types import int_pk_T
from src.models import BaseModel
from src.utils.enums import EventState


class Bet(BaseModel):
    __tablename__ = "bets"

    id: Mapped[int_pk_T]
    amount: Mapped[DECIMAL] = mapped_column(DECIMAL(10, 2))
    event_id: Mapped[int]
    state: Mapped[int] = mapped_column(Enum(EventState))
