import asyncio, os, handlers

from aiogram import Bot, Dispatcher
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from pybit.unified_trading import HTTP

from dotenv import load_dotenv


# logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)

default_deposit = 50000  # UAH


load_dotenv()
bot = Bot(token=os.getenv("DEV_TOKEN") or os.getenv("PROD_TOKEN"))


class Form(StatesGroup):
    asking_pair = State()
    asking_deposit = State()


session = HTTP(
    api_key="67GkDlaKlKzbrzWg6I",
    api_secret="zjtIt9oZW01JLCOBWhyRQjZq4kAW45G0nUrN",
)


async def main():
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(handlers.handlers.router)
    # dp.include_router(handlers.bundles.router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
