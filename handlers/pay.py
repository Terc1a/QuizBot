from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, ContentType
from create_bot import bot


async def order(message: Message, x):
    PRICE = [LabeledPrice(label='test', amount=int(x) * 100)]
    await bot.send_invoice(message.chat.id,
                           title='test',
                           description='test',
                           provider_token='381764678:TEST:49169',
                           currency='rub',
                           need_email=True,
                           prices=PRICE,
                           start_parameter='example',
                           payload='some_invoice')


async def pre_checkout_process(pre_checkout: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout.id, ok=True)


async def successful_payment(message: Message):
    await bot.send_message(message.chat.id, 'nice')



'''@dp.message_handler(state=FSMAdmin3.input)
async def solution(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        print('solution')
        zoz = str(message.text)
        data['input'] = zoz
        await FSMAdmin3.input.set()
        print(zoz, 'zoz')
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
            await asyncio.sleep(1)'''