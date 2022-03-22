from pydantic import BaseSettings

class Settings(BaseSettings):
    postgres_hostname: str
    postgres_port: str 
    postgres_user: str
    postgres_password: str
    postgres_db: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = "dev.env"

settings = Settings()