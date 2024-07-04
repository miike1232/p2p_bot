import sqlite3

from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

import keyboards as kb
from main import Form, bot

router = Router()

# =====================
#    - /start
#    - Добавить связку
#    - Депозит
#    - Текущий курс
#    - Обновить курс
# =====================


@router.message(CommandStart())
async def start_message(message: Message):
    await message.answer("Привет, выбери действие...", reply_markup=kb.main)


@router.message(F.text == 'Все связки')
async def unbroken_pairs(message: Message):
    wait_message = await message.answer("Подождите...")
    await message.answer(
        text="Все связки:",
        reply_markup=kb.get_unbroken_pairs_keyboard()
    )
    await bot.delete_message(chat_id=message.chat.id, message_id=wait_message.message_id)


@router.message(F.text == 'Поломанные связки')
async def broken_pairs(message: Message):
    wait_message = await message.answer("Подождите...")
    await message.answer(
        text="Поломанные связки:",
        reply_markup=kb.get_broken_pairs_keyboard()
    )
    await bot.delete_message(chat_id=message.chat.id, message_id=wait_message.message_id)


@router.message(F.text == 'Добавить связку')
async def asking_add_pair(message: Message, state: FSMContext):
    await message.answer("Напишите связку в формате (USDT-BTC-EUR):")
    await state.set_state(Form.asking_pair)


@router.message(Form.asking_pair)
async def add_pair(message: Message, state: FSMContext):
    try:
        currency1, currency2, currency3 = message.text.split("-")
    except ValueError:
        await message.answer("Неправильный формат. Используйте формат 'currency-currency-currency'.")
        return

    conn = sqlite3.connect('trading_pairs.db')
    cursor = conn.cursor()

    # Проверка существования связки
    cursor.execute('''
        SELECT 1 FROM pairs WHERE currency1 = ? AND currency2 = ? AND currency3 = ?
    ''', (currency1, currency2, currency3))

    if cursor.fetchone():
        await message.answer("Такая связка уже существует.")
    else:
        cursor.execute('''
            INSERT INTO pairs (currency1, currency2, currency3, is_broken)
            VALUES (?, ?, ?, ?)
        ''', (currency1, currency2, currency3, 0))
        conn.commit()
        await message.answer("Связка успешно добавлена.")
        await state.clear()

    conn.close()