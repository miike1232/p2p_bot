from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from main import session, default_deposit
from database import check_pairs, get_broken_pairs

main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Все связки')],
        [KeyboardButton(text='Добавить связку'), KeyboardButton(text='Поломанные связки')],
    ],
    resize_keyboard=True,
    input_field_placeholder='Выберите...'
)


def get_unbroken_pairs_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    pairs = check_pairs(session, default_deposit)
    pairs = sorted(pairs, key=lambda x: x['value'])
    for pair in pairs:
        keyboard_builder.button(
            text=f"{pair['name']} [{pair['value']}%]",
            callback_data=pair['name']
        )

    keyboard_builder.adjust(1)
    # keyboard_builder.adjust(2)
    return keyboard_builder.as_markup()


def get_positive_pairs_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    for p in check_pairs(session, default_deposit):
        if p['value'] > 0:
            keyboard_builder.button(
                text=f"{p['name']} [{p['value']}%]",
                callback_data=p['name']
            )

    keyboard_builder.adjust(1)
    # keyboard_builder.adjust(2)
    return keyboard_builder.as_markup()


def get_broken_pairs_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    for p in get_broken_pairs():
        name = f"{p[1]}-{p[2]}-{p[3]}"
        keyboard_builder.button(
            text=name,
            callback_data=name
        )

    keyboard_builder.adjust(1)
    # keyboard_builder.adjust(2)
    return keyboard_builder.as_markup()
