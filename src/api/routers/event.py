from fastapi import APIRouter, Depends

from src.schemas.event import EventSchema
from src.schemas.wrapper import EventListWrapper
from src.services.event import EventService
from src.utils.unit_of_work import UnitOfWork

router = APIRouter()


@router.get('/', tags=["events"])
async def get_events():
    events = await EventService.get_active_events()
    return EventListWrapper(
        payload=events
    )


@router.post('/', tags=["events"])
async def update_event(
    event: EventSchema,
    uow: UnitOfWork = Depends(UnitOfWork),
):
    await EventService.update_event_data(uow, event)
    return


@router.get('/{event_id}', tags=["events"])
async def get_events(event_id: int):
    events = await EventService.get_event_by_id(str(event_id))
    return EventListWrapper(
        payload=[events]
    )
