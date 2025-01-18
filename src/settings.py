from pydantic import AnyUrl, field_validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    weaviate_endpoint: AnyUrl
    weaviate_api_key: str
    cohere_api_key: str
    openai_api_key: str

    @field_validator('weaviate_endpoint')
    def validate_weaviate_domain(cls, v: AnyUrl) -> AnyUrl:
        if 'weaviate.cloud' not in v.host:
            raise ValueError('The URL must include "weaviate.cloud"')
        return v

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8' 

settings = Settings()