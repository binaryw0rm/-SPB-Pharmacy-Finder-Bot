import os
import sys
from dotenv import load_dotenv

load_dotenv(override=True)

BOT_TOKEN = os.getenv("BOT_TOKEN")
# Получаем ADMIN_ID, убираем пробелы, если есть
admin_env = os.getenv("ADMIN_ID", "")
ADMIN_ID = str(admin_env).strip() if admin_env else None

if not BOT_TOKEN:
    print("❌ CRITICAL ERROR: BOT_TOKEN не найден в .env!")
    sys.exit(1)

CSV_PATH = os.path.join("data", "pharmacies.csv")
LOG_FILE = os.path.join("logs", "bot.log")