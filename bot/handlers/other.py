from aiogram import Dispatcher
from aiogram.types import Message


async def echo(msg: Message):
    text = "Вибачте, я Вас не розумію!\n\n<i>Використайте /menu або /help</i>"
    await msg.answer(text)


def register_other_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(echo, content_types=['text','photo'])