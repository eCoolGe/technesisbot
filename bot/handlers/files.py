import pandas as pd
from io import BytesIO

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, CommandStart

from ..keyboards import files_kb, cancel_kb
from ..logger import log
from ..config import bot
from ..connections import db
from ..lang.ru import (
    MSG_HELLO,
    MSG_SEND_FILE,
    MSG_CANCEL
)
from ..callbacks.actions import FilesAction, CancelAction
from ..callbacks import FilesData, CancelData
from ..models.handlers import SendFile
from ..models.db import Record

router = Router()


# region Команда /start
@router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext):
    """
    Отвечает приветственным сообщением на стартовую команду и требует согласиться с положением о персональных данных
    """
    await state.clear()
    # telegram_id = message.from_user.id
    # username = message.from_user.username

    await message.reply(MSG_HELLO, reply_markup=files_kb().as_markup())
# endregion

@router.callback_query(FilesData.filter(F.action == FilesAction.upload))
async def files_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(callback.message.text)
    await callback.message.answer(
        text=MSG_SEND_FILE,
        reply_markup=cancel_kb().as_markup(),
    )
    await state.set_state(SendFile.set_file)
    await callback.answer()



@router.message(SendFile.set_file, F.content_type.in_({"document"}))
async def send_file_set(message: Message, state: FSMContext):
    """
    Обработка добавления к вопросу документа или текста
    """
    if not message.document.file_name.endswith(".xlsx"):
        await message.answer("Некорректный файл. Данный файл имеет неправильное расширение, требуется .xlsx")
        return

    file_data = await bot.download(message.document.file_id)
    df = pd.read_excel(BytesIO(file_data.getvalue()))

    if not all(col in df.columns for col in ["title", "url", "xpath"]):
        await message.answer("Некорректный файл. Должны быть столбцы: title, url, xpath")
        return

    df_table = df.to_markdown(index=False)

    df.to_sql(Record.__tablename__, con=db.engine, if_exists="append", index=False)

    await message.answer(f"Файл добавлен \n <pre>{df_table}</pre>")
    await state.clear()

@router.callback_query(SendFile.set_file, CancelData.filter(F.action == CancelAction.cancel))
async def send_file_cancel(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(callback.message.text)
    await callback.message.answer(
        text=MSG_CANCEL,
    )
    await state.set_state(SendFile.set_file)
    await callback.answer()