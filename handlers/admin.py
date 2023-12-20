from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, \
    InlineKeyboardButton

from create_bot import dp, bot
from database import database_conn
from keyboards import admin_kb

ID = None


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    solve = State()
    id = State()
    type = State()
    price = State()
    time = State()


# Получаем id админа
@dp.message_handler(commands=['m'])
async def make_changes_command(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Буду служить вам до самой смерти, господин',
                           reply_markup=admin_kb.button_case_admin)
    """ , reply_markup=button_case_admin) """
    await message.delete()


async def cm_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await message.reply('Загрузите фото')



async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('OK')
        await FSMAdmin.photo.set()


# Ловим ответ и пишем в словарь
@dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await FSMAdmin.name.set()
    await message.reply('Теперь напишите название игры')
    print('succ 1')


# Ловим второй ответ
@dp.message_handler(content_types=['name'], state=FSMAdmin.name)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdmin.description.set()
    await message.reply('Теперь добавьте задание игры')
    print('succ 2')


@dp.message_handler(content_types=['description'], state=FSMAdmin.description)
async def load_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await FSMAdmin.solve.set()
    await message.reply('Теперь добавьте ответ этой игры')
    print('succ 3')


@dp.message_handler(content_types=['solve'], state=FSMAdmin.solve)
async def load_solve(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['solve'] = message.text
    await FSMAdmin.id.set()
    await message.reply('Теперь добавьте айди этой игры')
    print('succ 4')


@dp.message_handler(content_types=['id'], state=FSMAdmin.id)
async def load_game(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = message.text

    async with state.proxy() as data:
        await message.reply(str(data))
    print('succ 5')
    await database_conn.sql_add_command2(state)
    await message.reply('Теперь укажите тип игры')
    await FSMAdmin.type.set()


@dp.message_handler(content_types=['type'], state=FSMAdmin.type)
async def load_type(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['type'] = message.text
    await FSMAdmin.price.set()
    await message.reply('Теперь добавьте стоимость игры')
    print('succ 6')


@dp.message_handler(content_types=['price'], state=FSMAdmin.price)
async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
    await FSMAdmin.time.set()
    await message.reply('Теперь добавьте время игры')
    print('succ 7')


@dp.message_handler(content_types=['time'], state=FSMAdmin.time)
async def load_time(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['time'] = message.text
    async with state.proxy() as data:
        await message.reply(str(data))
    print('succ 8')

    await database_conn.sql_add_command3(state)
    await state.finish()


# Удаление записи
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callback_run(callback_query: types.CallbackQuery):
    await database_conn.sql_delete_command(callback_query.data.replace("del ", ""))
    await callback_query.answer(text=f'запись удалена', show_alert=True)


@dp.message_handler(commands='Удалить')
async def delete_item(message: types.Message):
    if message.from_user.id == ID:
        read = await database_conn.sql_read2()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]} {ret[2]}')
            await bot.send_message(message.from_user.id, text='^^^', reply_markup=InlineKeyboardMarkup(). \
                                   add(InlineKeyboardButton(f'Удалить {ret[1]}', callback_data=f'del {ret[1]}')))
            return delete_item


# Регистрируем хендлеры
def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cm_start, commands=['Загрузить'], state=None)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_solve, state=FSMAdmin.solve)
    dp.register_message_handler(load_type, state=FSMAdmin.type)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(load_game, state=FSMAdmin.id)
    dp.register_message_handler(load_time, state=FSMAdmin.time)
    dp.register_message_handler(cancel_handler, commands='отмена', state="*")
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state='*')
    dp.register_message_handler(make_changes_command, commands=['m'], is_chat_admin=True)
