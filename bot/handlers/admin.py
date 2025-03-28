from aiogram import Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command

from ..config import settings
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