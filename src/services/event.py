from typing import List, Optional, TYPE_CHECKING

import aiohttp
from fastapi import status

from src.config import settings
from src.schemas.event import EventSchema
from src.services.redis import RedisService
if TYPE_CHECKING:
    from src.services.bet import BetService


class EventService:
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

    @staticmethod
    async def update_event_data(event: EventSchema) -> None:
        RedisService.add_or_update_in_cache(str(event.id), event)

        #TODO: вызов сервиса ставок для обновления статуса
