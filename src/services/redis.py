import pickle
from typing import Any, List

from redis import Redis

from src.config import settings
from src.schemas.event import EventSchema


cache = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    password=settings.REDIS_PASSWORD,
)


class RedisService:
    @staticmethod
    def store_events(events: List[EventSchema]) -> None:
        with cache.pipeline() as pipe:
            for event in events:
                pipe.set(
                    str(event.id),
                    pickle.dumps(event),
                    ex=settings.REDIS_CACHING_TIME,
                )
            pipe.execute()

    @staticmethod
    def get_from_cache(key: str) -> Any:
        cached = cache.get(key)
        if not cached:
            return
        return pickle.loads(cached)

    @staticmethod
    def add_or_update_in_cache(key: str, data: Any) -> None:
        cache.set(key, pickle.dumps(data), ex=settings.REDIS_CACHING_TIME)
