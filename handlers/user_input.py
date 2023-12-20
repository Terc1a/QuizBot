from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from create_bot import bot, dp
from aiogram import Bot
from aiogram import Dispatcher, types
from database import database_conn
from handlers.client import kb_client

class FSMAdmin3(StatesGroup):
    input = State()


@dp.message_handler(state=FSMAdmin3.input)
async def solution(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        print('solution')
        zoz = str(message.text)
        data['input'] = zoz
        for check in checker:
            print(check, 'check')
        print(zoz, 'input')
        riad = await database_conn.sql_select_command8(check)
        for rut in riad:
            print(rut, 'rut')
        for y in rut:
            # y = str(rut[0])
            print(y, 'igrek')
        if y == zoz:
            print('yes')
            await bot.send_message(chat_id='-1001781599983', text='правильный ответ')
            await message.answer(text='вы победили, вы можете вывести деньги по кнопке  Вывести')
        else:
            print('no')
            await bot.send_message(chat_id='-1001781599983', text='неверно')
        if True:
            schedule.add_job(kick_user.kick_user, trigger='interval', seconds=60,
                             kwargs={'bot': bot, 'message': message})
            print('запустилось, но 3')
            await asyncio.sleep(1)