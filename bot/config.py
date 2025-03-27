from aiogram.client.default import DefaultBotProperties
from pydantic_settings import BaseSettings
from aiogram import Bot

from .models.config import EnvSettingsModel, DatabaseParamsModel


_env_settings = EnvSettingsModel()


class BotConfig(BaseSettings):
    """
    Описывает и хранит в себе все данные, которые нужны для работы всех остальных модулей, запросов и подключений
    """

    DB_PARAMS: DatabaseParamsModel = DatabaseParamsModel(
        path=_env_settings.db_path,
    )
    """Параметры для подключения к базе данных"""

    LOG_MODE: bool = _env_settings.log_mode
    """Включает или отключает логирование в группу"""

    LOG_GROUP_ID: int = _env_settings.log_group_id
    """ID группы, куда оправлять самые важные логи"""

    LOG_FILE_PATH: str = _env_settings.log_file_path
    """Путь к файлу, в который копируются логи из консоли"""

    TESTING_MODE: bool = _env_settings.testing_mode
    """Включает или отключает режим тестирования бота"""

    TRUSTED_ID: list[int] = [572564221]
    """Список доверенных пользователей, которые могут использовать Админ-команды"""


settings = BotConfig()
"""
Экземпляр конфиг-класса, в котором содержатся все настройки
"""
bot = Bot(token=_env_settings.bot_token.get_secret_value(), default=DefaultBotProperties(parse_mode='HTML'))
"""
Экземпляр бот-класса, который нужен для запуска самого бота, а также используется в некоторых других местах 
"""