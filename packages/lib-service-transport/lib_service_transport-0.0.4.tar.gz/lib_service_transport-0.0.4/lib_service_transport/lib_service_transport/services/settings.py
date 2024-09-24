from pydantic_settings import BaseSettings

from lib_service_transport.lib_service_transport.services.kafka.settings import KafkaSettings
from lib_service_transport.lib_service_transport.services.rabbit.settings import RabbitMQSettings


class Settings(BaseSettings):
    """Настройки библиотеки"""
    rabbit: RabbitMQSettings()
    kafka: KafkaSettings()
