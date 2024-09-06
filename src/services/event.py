import time
from typing import List, Optional, TYPE_CHECKING, Callable

import aiohttp
from fastapi import status

from src.config import settings
from src.schemas.event import EventSchema
from src.services.redis import RedisService
from src.utils.enums import EventState
from src.utils.unit_of_work import UnitOfWork

if TYPE_CHECKING:
    from src.services.bet import BetService


class EventService:
    on_update_callback: Optional[Callable] = None

    @staticmethod
    async def get_active_events() -> List[EventSchema]:
        async with aiohttp.ClientSession() as session:
            async with session.get(settings.GET_EVENTS_URL) as response:
                if not response.status == status.HTTP_200_OK:
                    return []

                events_data = (await response.json()).get("payload")

                if not events_data:
                    return []

                events = [
                    EventSchema(**event)
                    for event in events_data
                ]

                RedisService.store_events(events)

                return events

    @staticmethod
    async def get_event_by_id(event_id: str) -> Optional[EventSchema]:
        if not isinstance(event_id, str):
            event_id = str(event_id)

        event = RedisService.get_from_cache(event_id)
        if isinstance(event, EventSchema):
            return event

        url = settings.GET_SINGLE_EVENT_URL+event_id
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if not response.status == status.HTTP_200_OK:
                    return

                event = (await response.json()).get("payload")

                if not event:
                    return

                return EventSchema(**event)

    @classmethod
    async def update_event_data(
        cls,
        uow: UnitOfWork,
        event: EventSchema,
    ) -> None:
        RedisService.add_or_update_in_cache(str(event.id), event)

        if cls.on_update_callback:
            await cls.on_update_callback(uow, event.id, event.state)

    @classmethod
    def register_on_update_callback(cls, callback: Callable) -> None:
        cls.on_update_callback = callback

    @staticmethod
    async def check_if_event_valid(event_id: int) -> bool:
        event = await EventService.get_event_by_id(str(event_id))

        if (
            not event or
            int(time.time()) > event.deadline or
            event.state != EventState.NEW
        ):
            return False

        return True
