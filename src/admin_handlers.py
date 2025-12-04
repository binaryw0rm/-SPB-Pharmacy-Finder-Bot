from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from src.config import ADMIN_ID
from src.states import AddPharmStates, DelPharmStates
from src.db_loader import repo

router = Router()

def is_admin(message: types.Message):
    if not ADMIN_ID:
        return False
    return str(message.from_user.id) == ADMIN_ID

@router.message(Command("admin"))
async def cmd_admin(message: types.Message):
    if not is_admin(message):
        return
    
    text = (
        "🛠 <b>Admin Panel</b>\n\n"
        "/list_all - Список ВСЕХ аптек (с ID)\n"
        "/add_pharm - Добавить аптеку\n"
        "/del_pharm - Удалить аптеку по ID\n"
        "/cancel - Отмена"
    )
    await message.answer(text, parse_mode="HTML")

@router.message(Command("cancel"))
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Canceled.")

# --- СПИСОК ВСЕХ АПТЕК ---
@router.message(Command("list_all"))
async def list_all_pharmacies(message: types.Message):
    if not is_admin(message): return
    
    data = repo.data
    if not data:
        await message.answer("Список аптек пуст.")
        return

    # Формируем длинный текст
    lines = []
    lines.append(f"📦 <b>Всего аптек: {len(data)}</b>\n")
    
    for p in data:
        # Формат: ID | Название | Адрес
        line = f"🆔 <b>{p.get('id', '?')}</b> | {p.get('name', 'NoName')} | {p.get('address', 'NoAddr')}"
        lines.append(line)

    # Разбиваем на сообщения, если текст слишком длинный
    chunk_size = 4000
    full_text = "\n".join(lines)
    
    if len(full_text) <= chunk_size:
        await message.answer(full_text, parse_mode="HTML")
    else:
        # Если список очень длинный, шлем частями
        parts = [full_text[i:i+chunk_size] for i in range(0, len(full_text), chunk_size)]
        for part in parts:
            # Пытаемся закрыть тег bold, если он разрезался (простая защита)
            safe_part = part
            if safe_part.count("<b>") > safe_part.count("</b>"):
                safe_part += "</b>"
            await message.answer(safe_part, parse_mode="HTML")

# --- ДОБАВЛЕНИЕ ---
@router.message(Command("add_pharm"))
async def start_add(message: types.Message, state: FSMContext):
    if not is_admin(message): return
    await message.answer("Введите название аптеки:")
    await state.set_state(AddPharmStates.waiting_for_name)

@router.message(AddPharmStates.waiting_for_name)
async def add_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите адрес:")
    await state.set_state(AddPharmStates.waiting_for_address)

@router.message(AddPharmStates.waiting_for_address)
async def add_address(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    await message.answer("Введите район (Ex: Центральный):")
    await state.set_state(AddPharmStates.waiting_for_district)

@router.message(AddPharmStates.waiting_for_district)
async def add_district(message: types.Message, state: FSMContext):
    await state.update_data(district=message.text)
    await message.answer("Введите телефон:")
    await state.set_state(AddPharmStates.waiting_for_phone)

@router.message(AddPharmStates.waiting_for_phone)
async def add_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer("Режим работы (Ex: 24/7):")
    await state.set_state(AddPharmStates.waiting_for_hours)

@router.message(AddPharmStates.waiting_for_hours)
async def add_hours(message: types.Message, state: FSMContext):
    await state.update_data(working_hours=message.text)
    kb = types.ReplyKeyboardMarkup(keyboard=[
        [types.KeyboardButton(text="Yes"), types.KeyboardButton(text="No")]
    ], resize_keyboard=True, one_time_keyboard=True)
    await message.answer("Круглосуточно? (Yes/No)", reply_markup=kb)
    await state.set_state(AddPharmStates.waiting_for_24h)

@router.message(AddPharmStates.waiting_for_24h)
async def add_24h(message: types.Message, state: FSMContext):
    answer = message.text.lower()
    is_24 = True if answer in ['yes', 'да', 'true', '+'] else False
    await state.update_data(is_24h=is_24)
    
    kb = types.ReplyKeyboardMarkup(keyboard=[
        [types.KeyboardButton(text="📍 Send Location", request_location=True)]
    ], resize_keyboard=True)
    
    await message.answer("Отправьте локацию (Geolocation):", reply_markup=kb)
    await state.set_state(AddPharmStates.waiting_for_location)

@router.message(AddPharmStates.waiting_for_location, F.location)
async def add_coords(message: types.Message, state: FSMContext):
    lat = message.location.latitude
    lon = message.location.longitude
    data = await state.get_data()
    
    new_pharm = {
        "name": data['name'],
        "address": data['address'],
        "district": data['district'],
        "phone": data['phone'],
        "working_hours": data['working_hours'],
        "is_24h": data['is_24h'],
        "lat": lat,
        "lon": lon
    }
    
    new_id = repo.add_pharmacy(new_pharm)
    await message.answer(f"✅ Saved! ID: {new_id}", reply_markup=types.ReplyKeyboardRemove())
    await state.clear()

# --- УДАЛЕНИЕ ---
@router.message(Command("del_pharm"))
async def start_del(message: types.Message, state: FSMContext):
    if not is_admin(message): return
    await message.answer("Введите ID аптеки для удаления:")
    await state.set_state(DelPharmStates.waiting_for_id)

@router.message(DelPharmStates.waiting_for_id)
async def process_del(message: types.Message, state: FSMContext):
    pid = message.text.strip()
    if repo.delete_pharmacy(pid):
        await message.answer(f"✅ ID {pid} удален.")
    else:
        await message.answer(f"❌ ID {pid} не найден.")
    await state.clear()
