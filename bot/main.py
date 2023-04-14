from aiogram.utils import executor
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from AiogramTemplate.bot.database.methods import db_con
#from filters import register_all_filters
from AiogramTemplate.bot.misc import env
from AiogramTemplate.bot.handlers import register_all_handlers
from AiogramTemplate.bot.database.models import register_models


async def __on_start_up(dp: Dispatcher) -> None:
    #register_all_filters(dp)
    register_all_handlers(dp)
    register_models()


def start_bot():
    db_con.cur, db_con.con = db_con.get_connect()
    bot = Bot(token=env.TgKeys.TOKEN, parse_mode='HTML')
    dp = Dispatcher(bot, storage=MemoryStorage())
    executor.start_polling(dp, skip_updates=True, on_startup=__on_start_up)
