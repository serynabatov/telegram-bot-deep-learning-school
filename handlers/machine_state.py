from aiogram.dispatcher.filters.state import StatesGroup, State


class Machine_State(StatesGroup):
    # Выбран режим Гога
    Q1 = State()
    # Выбран режим трансфера
    Q2 = State()
    # Картинка выгружена
    Q3 = State()
