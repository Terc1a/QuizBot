from types import NoneType

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import state

from aiogram.utils import executor

import handlers
from create_bot import dp, bot
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ContentType, LabeledPrice, PreCheckoutQuery
from aiogram.dispatcher.filters.state import State, StatesGroup
import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from handlers import apsched, client, kick_user, payment
from database import database_conn
from handlers import pay

PAYMENTS_TOKEN = '381764678:TEST:49169'
b1 = KeyboardButton('/Оплатить', callback_data='user_id')
b2 = KeyboardButton('/Меню')
b3 = KeyboardButton('/Вывести', callback_data='user_balance')
kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_client.add(b1).add(b2).add(b3)
schedule = AsyncIOScheduler(timezone='Europe/Moscow')
types_list = {}


class FSMAdmin3(StatesGroup):
    type = State()
    input = State()
    price = State()


checker = {}


async def on_startup():
    schedule.start()
    print('стартануло')


@dp.message_handler(commands=['Оплатить'])
async def buy(message: types.Message):
    await message.answer(text='Выберите тип игры, который хотите оплатить:')
    await database_conn.sql_select_command6(message)
    await FSMAdmin3.type.set()


@dp.message_handler(state=FSMAdmin3.type)
async def state1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        machine_state = await state.get_state()
        print('123' + ' ' + machine_state)
        # print('state1')
        data['type'] = message.text
        types1 = await database_conn.sql_select_command10()
        for sel in types1:
            # print(sel,'sel')
            che = str(sel)
            # print(che, 'che')
            huy = data['type']
            # print(huy, 'huy')
            checker[huy] = data['type']
            # for check in checker:
            #    print(check, 'check')

            read = await database_conn.sql_select_command3(huy)
            for ret in read:
                # print(ret[0])
                for x in ret:
                    x = str(ret[0])
                    machine_state = await state.get_state()
                print('state1' + '\n' + machine_state + '\n' + message.text)
                await state.finish()

            # if che != huy:
            #    await message.reply('Тип игры введен неверно, выберите один из типов игр в списке')
            #    await state.finish()
            #    return buy
            if huy == 'Отмена':
                print('otmena')
                await client.cancel_handler(state)
                await message.reply('Отменено')
                await state.finish()
                return buy
            else:  # заменить else на if и добавить проверку
                func = await database_conn.sql_read4(message)
                for qut in func:
                    if qut != '' and qut is not None:
                        # print('true')
                        PRICE = [LabeledPrice(label='test', amount=int(x) * 100)]
                        await bot.send_invoice(message.chat.id, title='test', description='test',
                                               provider_token='381764678:TEST:49169',
                                               currency='rub', need_email=True, prices=PRICE,
                                               start_parameter='example',
                                               payload='some_invoice')


@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_process(pre_checkout: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await bot.send_message(message.chat.id, 'nice')
        if True:
            schedule.add_job(apsched.timer_message_cron, trigger='interval', seconds=9,
                             kwargs={'message': message})
            # print('запустилось')
            schedule.start()
            await asyncio.sleep(10)
            await bot.unban_chat_member(chat_id='-1001781599983', user_id='5870143609', only_if_banned=True)
            sex = data['type']
            # print(sex, 'sex2')
            read = await database_conn.sql_select_command7(sex)
            for ret in read:
                machine_state = await state.get_state()
                print('successfull payment' + '\n' + 'none' + '\n' + sex)
                # print(ret, 'ret2')
                await bot.send_message(chat_id='-1001781599983', text=ret[0] + '\n на ответ у вас есть 30 секунд')
                await FSMAdmin3.input.set()
                machine_state = await state.get_state()
                print('successfull payment_state' + ' ' + machine_state + ' ' + sex)


@dp.message_handler(state=FSMAdmin3.input)
async def solution(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        machine_state = await state.get_state()
        print('solution' + ' ' + machine_state)
        await bot.send_message(chat_id='-1001781599983', text='\n напишите ответ сюда')
        data['input'] = message.text
        print(data['input'])
        for check in checker:
            riad = await database_conn.sql_select_command8(check)
            machine_state = await state.get_state()
            if machine_state != NoneType:
                print('solution' + '\n' + machine_state + '\n' + message.text)
            else:
                print('solution' + '\n' + 'None' + '\n' + message.text)
            for rut in riad:
                for y in rut:
                    if y == data['type']:
                        # print('yes')
                        await bot.send_message(chat_id='-1001781599983', text='правильный ответ')
                        await message.answer(text='вы победили, вы можете вывести деньги по кнопке  Вывести')
                    else:
                        # print('no')
                        await bot.send_message(chat_id='-1001781599983', text='неверно')
                    if True:
                        schedule.add_job(kick_user.kick_user, trigger='interval', seconds=60,
                                     kwargs={'bot': bot, 'message': message})
                        print('запустилось, но 3')
                        await asyncio.sleep(1)


def register_handlers_ckb(dp: Dispatcher):
    dp.pre_checkout_query_handler(lambda query: True)
    dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
    dp.register_message_handler(buy)
    dp.register_message_handler(state1, state=FSMAdmin3.type)
    dp.register_message_handler(solution, state=FSMAdmin3.input)
    if __name__ == '__main__':
        executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
