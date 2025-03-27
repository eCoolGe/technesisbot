from ._generate_inline_keyboard import generate_inline_keyboard

from ..callbacks.actions import FilesAction
from ..callbacks import FilesData


def files_kb():
    """
    Клавиатура для работы с файлами
    """
    return generate_inline_keyboard(FilesAction, FilesData)