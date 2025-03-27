from aiogram.fsm.state import StatesGroup, State


class SendFile(StatesGroup):
    """
    Группа состояний, которая описывает взаимодействие загрузки файла
    """
    set_file = State()
