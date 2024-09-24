from pydantic import Field
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class KafkaSettings(BaseSettings):
    BOOTSTRAP_SERVERS: str = Field(default='localhost:9092')

    # Topics
    TOPIC_ORDER: str

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
        env_prefix='KAFKA_',
    )
