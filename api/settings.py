from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    pg_user: Optional[str] = None
    pg_pass: Optional[str] = None
    pg_host: Optional[str] = None
    pg_port: str = "5432"
    pg_db: Optional[str] = None

    is_unittest: bool = False


env = Settings()
