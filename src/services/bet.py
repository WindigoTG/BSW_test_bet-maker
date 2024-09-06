from fastapi import Depends

from src.schemas.bet import BetSchema, CreateBetSchema
from src.schemas.wrapper import BaseErrorWrapper, BaseWrapper, BetWrapper
from src.utils.enums import EventState
from src.utils.unit_of_work import UnitOfWork

from src.services.event import EventService

from src.utils.service import BaseService


class BetService(BaseService):
    base_repository: str = 'bet'

    @classmethod
    async def add_bet_and_get_response(
        cls,
        uow: UnitOfWork,
        bet: CreateBetSchema,
    ) -> BaseWrapper:
        is_event_valid = await EventService.check_if_event_valid(bet.event_id)

        if not is_event_valid:
            return BaseErrorWrapper(
                reason="Either the event doesn't exist or has expired.",
            )

        _obj = await cls.add_one_and_get_obj(
            uow,
            **bet.model_dump(),
            state=EventState.NEW,
        )

        if not _obj:
            return BaseErrorWrapper(
                reason="Unable to place bet.",
            )

        return BetWrapper(payload=BetSchema.model_validate(_obj), status=201)

    @classmethod
    async def on_update_event_state(
        cls,
        uow: UnitOfWork,
        event_id: int,
        state: EventState,
    ):
        async with uow:
            await uow.__dict__[
                cls.base_repository
            ].update_bets_state_by_event_id(event_id, state)


EventService.register_on_update_callback(BetService.on_update_event_state)
