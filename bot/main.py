from aiogram.utils import executor
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
import os

from .database.methods import database
#from filters import register_all_filters

from .handlers import register_all_handlers
from .database.models import register_models


async def __on_start_up(dp: Dispatcher) -> None:
    #register_all_filters(dp)
    register_all_handlers(dp)
    register_models()


def start_bot():
    logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w",
                        format="%(asctime)s %(levelname)s %(message)s")
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(log_format)

    logging.getLogger('').addHandler(console_handler)

    db = database()
    bot = Bot(token=os.environ.get("TOKEN"), parse_mode='HTML')
    dp = Dispatcher(bot, storage=MemoryStorage())
    executor.start_polling(dp, skip_updates=True, on_startup=__on_start_up)
