from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    DATABASE_URL: str = Field(default="")
    JWT_SECRET: str = Field(default="dev_jwt_secret_key_12345")
    HASH_PEPPER: str = Field(default="dev_hash_pepper_salt_98765")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=1440)

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
