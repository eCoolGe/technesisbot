from aiogram.types import Message

from ..config import settings
from . import IsAdmin


class IsTestingMode(IsAdmin):
    def __init__(self) -> None:
        """
        Фильтр, который запрещает использовать бота в режиме тестирования всем, кроме Администраторов
        """
        super().__init__()
        self.testing_mode = settings.TESTING_MODE

    async def __call__(self, message: Message) -> bool:
        if await super().__call__(message=message):
            return False

        log_message = (
            "[%s|%s] попытался использовать бота в режиме тестирования, выполнив действие: %s"
            if self.testing_mode
            else "[%s|%s] выполнил действие: %s"
        )
        self.log_info(message=message, log_message=log_message)
        return self.testing_mode