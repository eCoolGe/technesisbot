from aiogram import Dispatcher, types
from aiogram.filters import Command
from aiogram.types.error_event import ErrorEvent

from .lang.ru import (
    MSG_BROKEN_BOT,
    TEMPLATE_MSG_HELP,
)
from .handlers import files, admin, unknown
from .logs import custom_log
from .filters import IsTestingMode
from .logger import log

dp = Dispatcher()
dp.include_router(files.router)
dp.include_router(admin.router)
dp.include_router(unknown.router)


@dp.message(IsTestingMode())
async def process_block_if_testing_server(message: types.Message):
    """
    Не дает использовать команды бота всем кроме Администратора в том случае, если он в тестовом режиме
    """
    await message.reply(MSG_BROKEN_BOT)


@dp.message(Command("help"))
async def process_help_command(message: types.Message):
    """
    Отвечает списком команд и информацией об этих командах на команду /help
    """
    await message.reply(TEMPLATE_MSG_HELP)


@dp.errors()
async def process_errors(event: ErrorEvent):
    log.critical("Бот поймал критическую ошибку: %s", event.exception, exc_info=True)
    await custom_log(f"Бот поймал критическую ошибку: {event.exception}")