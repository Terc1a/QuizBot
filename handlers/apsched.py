from create_bot import bot, dp
from aiogram import types
from datetime import datetime, timedelta


async def timer_message_cron(message: types.Message):
    chat_id = '-1001781599983'
    expire_date = datetime.now() + timedelta(days=1)
    link = await bot.create_chat_invite_link(chat_id, expire_date.timestamp, 1)
    await bot.send_message(message.from_user.id, f'Игра вот-вот начнется! Заходи {link.invite_link}')
    print(link.invite_link)


#@dp.callback_query_handler(text=userid)
#async def user_id_inline_callback(callback_query: types.CallbackQuery):
#    await callback_query.answer(f"Ваш ID: {callback_query.from_user.id}", True)
