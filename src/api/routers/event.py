from fastapi import APIRouter

from src.schemas.event import EventSchema
from src.schemas.wrapper import EventListWrapper
from src.services.event import EventService

router = APIRouter()


@router.get('/')
async def get_events():
    events = await EventService.get_active_events()
    return EventListWrapper(
        payload=events
    )


@router.post('/')
async def update_event(event: EventSchema):
    await EventService.update_event_data(event)
    return


@router.get('/{event_id}')
async def get_events(event_id: int):
    events = await EventService.get_event_by_id(str(event_id))
    return EventListWrapper(
        payload=[events]
    )
