from aiogram import Dispatcher

from AiogramTemplate.bot.handlers.admin import register_admin_handlers
from AiogramTemplate.bot.handlers.other import register_other_handlers
from AiogramTemplate.bot.handlers.user import register_user_handlers


def register_all_handlers(dp: Dispatcher) -> None:
    handlers = (
        register_user_handlers,
        register_admin_handlers,
        register_other_handlers,
    )
    for handler in handlers:
        handler(dp)
