import asyncio

from .config import settings, bot
from .lang.ru import (
    LOG_MSG_DEFAULT_ERROR,
)
from .logs import custom_log
from .logger import log
from .dispatcher import dp


async def main():
    """
    Асинхронная бесконечная задача, цель которой: уведомить в лог-канал о запуске бота,
    подключить в фоне другие асинхронные задачи,
    запустить самого бота
    """

    while True:
        try:
            testing_mode = "включен" if settings.TESTING_MODE else "выключен"
            await custom_log(f"Бот запущен | Тестовый режим <b>{testing_mode}</b>")

            await dp.start_polling(bot, skip_updates=True)
        except Exception as e:
            log.error(LOG_MSG_DEFAULT_ERROR, e)
            await custom_log("Не удалось запустить бота")
            await asyncio.sleep(60 * 5)

def start():
    """
    Начальная точка, в которой начинается все что далее выполняется
    """
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log.info("Поймано прерывание с клавиатуры... Все процессы были остановлены!")


if __name__ == "__main__":
    start()