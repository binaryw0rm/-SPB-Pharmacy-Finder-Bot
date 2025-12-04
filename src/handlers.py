import logging
from aiogram import Router, F, types
from aiogram.filters import Command
from src.keyboards import main_menu, districts_kb, pharmacies_list_kb, route_kb
from src.db_loader import repo
from src.utils import get_google_maps_link

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Я помогу найти ближайшую круглосуточную аптеку в Санкт-Петербурге.\n"
        "Отправь свою геолокацию или выбери район.",
        reply_markup=main_menu()
    )

@router.message(Command("list"))
@router.message(F.text == "🏙 Выбрать район вручную")
async def cmd_list(message: types.Message):
    await message.answer("Выберите район поиска:", reply_markup=districts_kb())

@router.message(F.location)
async def handle_location(message: types.Message):
    user_lat = message.location.latitude
    user_lon = message.location.longitude

    try:
        pharmacy = repo.find_nearest(user_lat, user_lon, only_24h=True)

        if not pharmacy:
            await message.answer("К сожалению, круглосуточных аптек рядом не найдено. Попробуйте выбрать район вручную.")
            return

        # Формируем ответ
        text = (
            f"🏥 <b>{pharmacy['name']}</b>\n"
            f"📍 {pharmacy['address']}\n"
            f"🕒 Режим: {pharmacy['working_hours']}\n"
            f"📞 {pharmacy['phone']}\n"
            f"📏 Расстояние: {pharmacy['distance_km']} км"
        )

        # Ссылка на маршрут
        maps_url = get_google_maps_link(user_lat, user_lon, pharmacy['lat'], pharmacy['lon'])

        await message.answer_venue(
            latitude=float(pharmacy['lat']),
            longitude=float(pharmacy['lon']),
            title=pharmacy['name'],
            address=pharmacy['address']
        )
        await message.answer(text, parse_mode="HTML", reply_markup=route_kb(maps_url))
        
    except Exception as e:
        logging.error(f"Ошибка при поиске по локации: {e}")
        await message.answer("Произошла ошибка при поиске. Попробуйте позже.")

# Обработка выбора района
@router.callback_query(F.data.startswith("dist_"))
async def process_district(callback: types.CallbackQuery):
    district = callback.data.split("_")[1]
    pharmacies = repo.get_by_district(district, only_24h=True)

    if not pharmacies:
        await callback.message.answer(f"В районе {district} круглосуточных аптек не найдено.")
        await callback.answer()
        return

    await callback.message.answer(f"Найдено {len(pharmacies)} аптек в районе {district}:", 
                                  reply_markup=pharmacies_list_kb(pharmacies))
    await callback.answer()

# Обработка выбора конкретной аптеки из списка
@router.callback_query(F.data.startswith("pharm_"))
async def process_pharmacy_selection(callback: types.CallbackQuery):
    pharm_id = callback.data.split("_")[1]
    pharmacy = repo.get_by_id(pharm_id)

    if pharmacy:
        text = (
            f"🏥 <b>{pharmacy['name']}</b>\n"
            f"📍 {pharmacy['address']}\n"
            f"🕒 Режим: {pharmacy['working_hours']}\n"
            f"📞 {pharmacy['phone']}"
        )
        
        await callback.message.answer_venue(
            latitude=float(pharmacy['lat']),
            longitude=float(pharmacy['lon']),
            title=pharmacy['name'],
            address=pharmacy['address']
        )
        # Здесь мы не можем построить маршрут от пользователя, так как не знаем его координат,
        # поэтому просто выводим инфо. Можно добавить кнопку "Показать на карте" без маршрута.
        await callback.message.answer(text, parse_mode="HTML")
    else:
        await callback.message.answer("Информация об аптеке не найдена.")
    
    await callback.answer()