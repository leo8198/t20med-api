from pydantic import BaseSettings
from functools import lru_cache
from typing import List
from passlib.context import CryptContext


# File that contains all the repo configurations
class BaseConfig(BaseSettings):
    environment: str = "testing"
    secret_key: str
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    jwt_algorithm: str = "HS256"
    super_user_email: str
    super_user_username: str
    sendgrid_sender_email: str 
    sendgrid_api_key: str
    reset_password_endpoint: str
    zapsign_api_key: str
    my_api_url: str
    aws_bucket_name: str
    test_cpf: str
    redis_url: str
    aws_access_key_id: str
    aws_secret_access_key: str
    gotenberg_url: str

    class Config:
        env_file = ".env"

class ProductionSettings(BaseConfig):
    database_url: str

class DevelopmentSettings(ProductionSettings):
    api_test_url: str
    username_test: str
    password_test: str
    doctorname_test: str


class TestSettings(DevelopmentSettings):
    pass

@lru_cache
def get_settings():
    configs = {
        "production": ProductionSettings,
        "development": DevelopmentSettings,
        "testing": TestSettings
    }
    environment = BaseConfig().environment

    return configs[environment]()

settings = get_settings()