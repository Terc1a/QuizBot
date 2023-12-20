from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()


PAYMENTS_TOKEN = '401643678:TEST:0e3023a7-75ad-4ae5-8ab9-fc23eb088b53'
bot = Bot(token='5655918097:AAFHIa84UNGY8VZ5I4FQoJ6T6EiOIxIDv3I')
dp = Dispatcher(bot, storage=storage)
