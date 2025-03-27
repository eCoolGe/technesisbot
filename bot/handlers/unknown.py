from aiogram import F, Router, types

from ..lang.ru import MSG_ERROR_COMMAND

router = Router()


@router.message(F.content_type.in_({'text', 'any', 'photo', 'sticker', 'video', 'audio', 'document'}))
async def incorrect_command(message: types.Message):
    """
    Обработка неизвестных команд, которые не упали ни в один хендлер
    """
    await message.reply(MSG_ERROR_COMMAND)