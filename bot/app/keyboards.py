from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests import get_collections, get_collection_painting

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Коллекции и доступные картины музея')],
        [KeyboardButton(text='Дополнительные источники информации')],
        [KeyboardButton(text='Язык')], 
        [KeyboardButton(text='Помощь')]
    ],
    resize_keyboard=True,
    input_field_placeholder='Выберите пункт меню...'
)


async def collections():
    all_collections = await get_collections()
    keyboard = InlineKeyboardBuilder()
    for collection in all_collections:
        keyboard.add(InlineKeyboardButton(text=collection.name, callback_data=f"collection_{collection.id}"))
    keyboard.add(InlineKeyboardButton(text='⬅️ На главную', callback_data='to_main_menu'))
    return keyboard.adjust(1).as_markup()


async def paintings(category_id):
    all_paintings = await get_collection_painting(category_id)
    keyboard = InlineKeyboardBuilder()
    for painting in all_paintings:
        keyboard.add(InlineKeyboardButton(text=painting.name, callback_data=f"painting_{painting.id}"))
    keyboard.add(InlineKeyboardButton(text='⬅️ Коллекции', callback_data='to_all_collections'))
    return keyboard.adjust(1).as_markup()
