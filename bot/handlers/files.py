import pandas as pd
from io import BytesIO

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart

from ..connections.sites import parse_and_calculate_average
from ..keyboards import files_kb, cancel_kb
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
    Обрабатывает команду /start, отправляет приветственное сообщение и требует согласиться с положением о персональных данных.

    Args:
        message (Message): Сообщение, содержащее команду /start.
        state (FSMContext): Контекст состояния конечного автомата.
    """
    await state.clear()
    await message.reply(MSG_HELLO, reply_markup=files_kb().as_markup())
# endregion

@router.callback_query(FilesData.filter(F.action == FilesAction.upload))
async def files_callback(callback: CallbackQuery, state: FSMContext):
    """
    Обрабатывает нажатие на кнопку загрузки файла.

    Args:
        callback (CallbackQuery): Объект обратного вызова.
        state (FSMContext): Контекст состояния конечного автомата.
    """
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
    Обрабатывает добавление к вопросу документа или текста.

    Args:
        message (Message): Сообщение, содержащее документ.
        state (FSMContext): Контекст состояния конечного автомата.
    """
    if not message.document.file_name.endswith(".xlsx"):
        await message.answer("Некорректный файл. Данный файл имеет неправильное расширение, требуется .xlsx")
        return

    file_data = await bot.download(message.document.file_id)
    df = pd.read_excel(BytesIO(file_data.getvalue()))

    if not all(col in df.columns for col in ["title", "url", "xpath"]):
        await message.answer("Некорректный файл. Должны быть столбцы: title, url, xpath")
        return

    df.to_sql(Record.__tablename__, con=db.engine, if_exists="append", index=False)

    await message.answer(f"Файл успешно сохранен в бд! Выполняю цен... \n <pre>{df}</pre>")

    average_prices, site_prices = await parse_and_calculate_average(df)

    df_prices = pd.DataFrame(site_prices, columns=["Название", "Сайт", "Цена"])
    await message.answer(f"Парсинг цен по сайтам: \n <pre>{df_prices}</pre> \n <i>Если в поле \"Цена\" стоит \"-\",  - не удалось получить цену на сайте. Проверьте URL и XPath сайта</i>")
    if average_prices.items():
        df_avg = pd.DataFrame(average_prices.items(), columns=["Название", "Средняя цена"])
    else:
        df_avg = "Данные некорректны, проверьте URL и XPath ваших сайтов"

    await message.answer(f"Средняя цена по товарам: \n <pre>{df_avg}</pre>")

    await state.clear()

@router.callback_query(SendFile.set_file, CancelData.filter(F.action == CancelAction.cancel))
async def send_file_cancel(callback: CallbackQuery, state: FSMContext):
    """
    Обрабатывает нажатие на кнопку отмены загрузки файла.

    Args:
        callback (CallbackQuery): Объект обратного вызова.
        state (FSMContext): Контекст состояния конечного автомата.
    """
    await callback.message.edit_text(callback.message.text)
    await callback.message.answer(
        text=MSG_CANCEL,
    )
    await state.set_state(SendFile.set_file)
    await callback.answer()