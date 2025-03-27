from aiogram.filters.callback_data import CallbackData

from .actions import FilesAction


class FilesData(CallbackData, prefix="files"):
    action: FilesAction