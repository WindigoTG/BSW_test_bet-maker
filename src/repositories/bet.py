from sqlalchemy import update

from src.models import Bet
from src.utils.enums import EventState
from src.utils.repository import SqlAlchemyRepository


class BetRepository(SqlAlchemyRepository):
    model = Bet

    async def update_bets_state_by_event_id(
        self,
        event_id: int,
        event_state: EventState,
    ):
        query = update(self.model).filter(
            self.model.event_id == event_id,
        ).values(state=event_state)
        await self.session.execute(query)
