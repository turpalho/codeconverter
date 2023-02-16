from aiogram.fsm.state import State, StatesGroup


class CodeWriteState(StatesGroup):
    waiting_enter_code = State()