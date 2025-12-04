import asyncio
import logging
import os
import sys

# Добавляем корневую папку в путь (на всякий случай)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from aiogram import Bot, Dispatcher
from src.config import BOT_TOKEN, LOG_FILE
# Импортируем оба роутера
from src.handlers import router as user_router
from src.admin_handlers import router as admin_router

if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    # Сначала подключаем админку, потом юзера (порядок важен, чтобы админские команды ловились первыми)
    dp.include_router(admin_router)
    dp.include_router(user_router)
    
    logging.info("Инициализация бота...")
    
    await bot.delete_webhook(drop_pending_updates=True)
    
    # Яркое сообщение в терминал (Goal 1)
    print("\n" + "="*40)
    print("🚀 БОТ УСПЕШНО ЗАПУЩЕН И ГОТОВ К РАБОТЕ!")
    print(f"📡 Polling started...")
    print("="*40 + "\n")
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Бот остановлен администратором.")