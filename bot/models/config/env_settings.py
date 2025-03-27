from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvSettingsModel(BaseSettings):
    """
    Класс для модуля Pydantic, необходимый для считывая секретных данных из .env файла
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    bot_token: SecretStr
    log_mode: bool
    log_group_id: int
    log_file_path: str
    db_path: str
    testing_mode: bool
