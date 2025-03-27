import asyncio
import re
from aiogram import Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from aiogram.utils.chat_action import ChatActionSender

from ..config import settings, bot
from ..connections import db
from ..filters import IsAdmin


router = Router()


@router.message(Command("logs"), IsAdmin())
async def process_logs_command(message: Message):
    """
    Админ-команда: отправляет Администратору лог событий бота
    """
    await message.answer_document(FSInputFile(settings.LOG_FILE_PATH))


@router.message(Command("reset"), IsAdmin())
async def process_users_command(message: Message):
    """
    Админ-команда: пересоздает базу данных
    """
    db.reset_database()
    await message.answer(
        text=f"База данных пересоздана"
    )


    # async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id, interval=1):
    #     users = db.select_all_users()
    #     await message.answer(
    #         text=f"Ожидайте, уникальные записи пользователей <b>[{len(users)}]</b> будут выведены с интервалами 2 секунды..."
    #     )
    #     await asyncio.sleep(2)
    #     for user in users:
    #         await message.answer(text=str(user))
    #         await asyncio.sleep(2)