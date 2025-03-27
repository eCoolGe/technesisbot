from aiogram.utils.keyboard import InlineKeyboardBuilder


def generate_inline_keyboard(action_enum, data_type, **kwargs) -> InlineKeyboardBuilder:
    """Генерирует ин-лайн клавиатуру для заданного типа действий

    Args:
        action_enum: Обычно, Enum, который описывает действия на клавиатуре
        data_type: Тип данных (callback) для действий на клавиатуре
        **kwargs: Остальные аргументы callback, кроме action
    """
    builder = InlineKeyboardBuilder()
    for action in action_enum:
        builder.button(
            text=action.value,
            callback_data=data_type(action=action, **kwargs),
        )
    return builder