from typing import Optional
# from pydantic_settings import BaseSettings

class DatabaseSettings():
    MONGODB_URL: str = "mongodb://127.0.0.1:27017"
    MONGODB_DB_NAME: str = "crm_orchestra"
    MONGODB_DIRECT_CONNECTION: bool = True
    MONGODB_SERVER_SELECTION_TIMEOUT_MS: int = 2000

    class Config:
        env_file = ".env"

db_settings = DatabaseSettings() 