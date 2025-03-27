from aiogram.types import Message
from aiogram.filters import Filter

from ..logger import log
from ..config import settings


class IsAdmin(Filter):
    def __init__(self, logging: bool = False) -> None:
        """Фильтр для проверки у пользователя прав Администратора

        Args:
            logging (bool, optional): Отображать ли логи о том, что Администратор выполнил действие. Изначально равно True
        """
        self.admin_list = settings.TRUSTED_ID
        self.logging = logging

    @staticmethod
    def log_info(message: Message, log_message="Администратор [%s|%s] выполнил действие: %s"):
        log.info(
            log_message,
            message.from_user.id,
            message.from_user.username,
            message.text,
        )

    async def __call__(self, message: Message) -> bool:
        is_admin = message.from_user.id in self.admin_list
        if is_admin and self.logging:
            self.log_info(message=message)
        return is_admin