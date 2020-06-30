import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.executor import start_webhook
import asyncio
from aiogram.dispatcher.webhook import SendMessage
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os

API_TOKEN = os.environ.get('API_TOKEN')

event_loop = asyncio.get_event_loop()

# Конфигурируем логирование
logging.basicConfig(level=logging.DEBUG)

# Инициализируем бота и диспетчера
storage = MemoryStorage()
bot = Bot(token=API_TOKEN, loop=event_loop)
dp = Dispatcher(bot, storage=storage)


if __name__ == "__main__":
    from commands_bot import dp
    executor.start_polling(dp, loop=event_loop, skip_updates=True)

