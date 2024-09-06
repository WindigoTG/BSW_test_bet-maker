from fastapi import APIRouter, Depends

from src.schemas.bet import BetSchema, CreateBetSchema
from src.schemas.wrapper import BetListWrapper
from src.services.bet import BetService
from src.utils.unit_of_work import UnitOfWork

router = APIRouter()


@router.get(
    '/bets',
    summary="Get list of bets.",
    tags=["bets"]
)
async def get_bets(uow: UnitOfWork = Depends(UnitOfWork)):
    """Get list of bets."""
    bets = await BetService.get_by_query_all(uow)
    return BetListWrapper(
        payload=[
            BetSchema.model_validate(bet)
            for bet in bets
        ]
    )


@router.post(
    '/bet',
    summary="Place a bet on an event.",
    tags=["bets"],
)
async def place_bet(
    bet: CreateBetSchema,
    uow: UnitOfWork = Depends(UnitOfWork)
):
    """
    Place a bet on an event.

    Body params:
    - **amount**: Amount to bet on the event.
    - **event_id**: Id of the event.
    """
    response = await BetService.add_bet_and_get_response(uow, bet)
    return response
