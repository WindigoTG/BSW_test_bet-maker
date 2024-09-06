from dotenv import find_dotenv, load_dotenv

from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    MODE: str = 'DEV'

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    REDIS_CACHING_TIME: int = 3600

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


load_dotenv(find_dotenv('.env'))
settings = Settings()
