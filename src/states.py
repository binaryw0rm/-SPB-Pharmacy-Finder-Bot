from aiogram.fsm.state import State, StatesGroup

class AddPharmStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_address = State()
    waiting_for_district = State()
    waiting_for_phone = State()
    waiting_for_hours = State()
    waiting_for_24h = State()
    waiting_for_location = State()

class DelPharmStates(StatesGroup):
    waiting_for_id = State()