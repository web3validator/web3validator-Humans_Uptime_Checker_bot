from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateChecker(StatesGroup):
    """States for checker creating form"""

    chain = State()
    operator_address = State()


class EditChecker(StatesGroup):
    """States for checker creating form"""

    chain = State()
    operator_address = State()


class DeleteChecker(StatesGroup):
    """States for checker creating form"""

    chain = State()
    operator_address = State()

class Status(StatesGroup):
    
    moniker = State()
    operator_address = State()
