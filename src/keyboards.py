from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def main_menu():
    kb = [
        [KeyboardButton(text="📍 Отправить геолокацию", request_location=True)],
        [KeyboardButton(text="🏙 Выбрать район вручную")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def districts_kb():
    districts = ["Центральный", "Московский", "Выборгский", "Крестовский"]
    builder = InlineKeyboardBuilder()
    for d in districts:
        builder.button(text=d, callback_data=f"dist_{d}")
    builder.adjust(2)
    return builder.as_markup()

def pharmacies_list_kb(pharmacies):
    builder = InlineKeyboardBuilder()
    for p in pharmacies:
        # В callback_data передаем ID аптеки
        builder.button(text=f"{p['name']} ({p.get('address', 'Нет адреса')})", callback_data=f"pharm_{p['id']}")
    builder.adjust(1)
    return builder.as_markup()

def route_kb(url):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🗺 Построить маршрут (Google Maps)", url=url)]
    ])