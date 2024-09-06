from src.models import Bet
from src.utils.repository import SqlAlchemyRepository


class BetRepository(SqlAlchemyRepository):
    model = Bet
