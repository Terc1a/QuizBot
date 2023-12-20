from os import link
from aiogram import types
from aiogram.utils import executor
import hashlib
from handlers import client, admin
from keyboards import client_kb

from create_bot import dp
import requests
from database import database_conn

"""MethodGetUpdates = 'https://api.telegram.org/bot5655918097:AAGoOiVHZsbQdTfk0fUW798szIfMZV9kJ7s/getUpdates'.format(
    token='5655918097:AAFHIa84UNGY8VZ5I4FQoJ6T6EiOIxIDv3I')
while True:
    response = requests.post(MethodGetUpdates)
    result = response.json()
    print(result)"""


async def on_startup(_):
    print('Бот вышел в онлайн, прям как твой батя за хлебом')
    database_conn.sql_start()


client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
client_kb.register_handlers_ckb(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
