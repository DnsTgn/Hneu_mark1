from aiogram import executor
from bot.main import start_bot

if __name__ == '__main__':
    executor.start_polling(start_bot())
