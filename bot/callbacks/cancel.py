from aiogram.filters.callback_data import CallbackData

from .actions import CancelAction


class CancelData(CallbackData, prefix="cancel"):
    action: CancelAction