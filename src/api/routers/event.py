from fastapi import APIRouter, Depends

from src.schemas.event import EventSchema
from src.schemas.wrapper import EventListWrapper
from src.services.event import EventService
from src.utils.unit_of_work import UnitOfWork

router = APIRouter()


@router.get(
    '/',
    summary="Get list of active events.",
    response_model=EventListWrapper,
    tags=["events"],
)
async def get_events():
    """Get list of active events."""
    events = await EventService.get_active_events()
    return EventListWrapper(
        payload=events
    )


@router.post(
    '/',
    summary="Endpoint for notifications about changes in events.",
    tags=["events"],
)
async def update_event(
    event: EventSchema,
    uow: UnitOfWork = Depends(UnitOfWork),
):
    """
    Endpoint for notifications about changes in events.

    Body params:
    - **id**: Id of the event.
    - **coefficient**: Bet coefficient for the event.
    - **deadline**: Timestamp of betting dedline.
    - **state**: State of the event.
    """
    await EventService.update_event_data(uow, event)
    return


@router.get('/{event_id}', tags=["events"])
async def get_events(event_id: int):
    events = await EventService.get_event_by_id(str(event_id))
    return EventListWrapper(
        payload=[events]
    )
