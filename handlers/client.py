
from aiogram.dispatcher.filters import Text
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils import executor
import logging

from create_bot import dp
from create_bot import bot
from database import database_conn
from keyboards import kb_client
from apscheduler.schedulers.asyncio import AsyncIOScheduler

schedule = AsyncIOScheduler(timezone='Europe/Moscow')
user_id_list = {}
global base, cur
global ID
class FSMAdmin2(StatesGroup):
    price = State()
    type = State()
    text = State()


async def start(message: types.Message):
    schedule.start()
    print('стартануло')


logging.basicConfig(level=logging.INFO)


async def cancel_handler(state: FSMContext):
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()


async def command_start(message: types.Message, state: FSMContext):
    if not user_id_list.get(message.from_user.id):
        userid = message.from_user.id
        user_id_list[userid] = []
        print(*user_id_list)
        # Сохраняем информацию о её владельце для быстрого поиска в дальнейшем
        async with state.proxy() as data:
            user_id_list[userid] = str(message.from_user.id)
            data['user_id'] = user_id_list[userid]
            data['user_balance'] = 0
        await bot.send_message(message.from_user.id, 'Добро пожаловать в квиз-бота,\n'
                                                     'по кнопкам ниже вы можете ознакомиться с правилами, лицензионным соглашением и сделать первый взнос',
                               reply_markup=kb_client)
        await database_conn.sql_add_command(state)
        await state.finish()


async def command_print(message: types.Message):
    await bot.send_message(message.from_user.id, f'Доступно для вывода 0 рублей')
    # Выключаем состояние


async def bot_menu_command(message: types.Message):
    await database_conn.sql_read(message)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(cancel_handler, commands='Отмена', state="*")
    dp.register_message_handler(cancel_handler, Text(equals='Отмена', ignore_case=True), state='*')
    dp.register_message_handler(command_start, commands=['start'])
    #dp.register_message_handler(command_buy, commands=['Оплатить'])
    dp.register_message_handler(bot_menu_command, commands=['Меню'])
    dp.register_message_handler(command_print, commands=['Вывести'])
    """ dp.register_message_handler(wrong_command) """


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=start)
