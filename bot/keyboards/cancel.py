from ._generate_inline_keyboard import generate_inline_keyboard

from ..callbacks.actions import CancelAction
from ..callbacks import CancelData


def cancel_kb():
    """
    Клавиатура для отмены действия
    """
    return generate_inline_keyboard(CancelAction, CancelData)