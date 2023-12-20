import asyncio

from create_bot import bot
from aiogram import types, Bot
import requests

from handlers import client


async def kick_user(bot: Bot, message: types.Message):
    chat_id = '-1001781599983'
    user_id = int(*client.user_id_list)
    message_id = message.message_id
    print(message_id)
    await bot.kick_chat_member(chat_id, user_id, until_date=None)
    # unban_chat_member доделать
    await bot.unban_chat_member(chat_id, user_id)
    if True:
        await asyncio.sleep(5)
        # на всякий случай проверяем есть ли еще сообщение
        try:
            await bot.delete_message(chat_id, message_id)
        except Exception as e:
            pass
        print('кикнуто')
