from bot.main import start_bot
from bot.database.methods.db import set_base

if __name__ == '__main__':
    set_base()
    start_bot()