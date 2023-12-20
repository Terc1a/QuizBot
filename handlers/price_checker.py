from aiogram import types
from aiogram.dispatcher import FSMContext

from database import database_conn




async def check_price(state: FSMContext):
    async with state.proxy() as data:
        PRICE = types.LabeledPrice(label='Участие в одной игре', amount=data['price'] * 100)
        await database_conn.sql_add_command3(state)
        await state.finish()
