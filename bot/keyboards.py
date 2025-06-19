from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.db_requests import get_collections, get_collection_painting


main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Найти картину по коллекции музея')],
        [KeyboardButton(text='Найти картину по названию')],
        [KeyboardButton(text='Найти картину по фотографии')],
    ],
    resize_keyboard=True,
    input_field_placeholder='Выберите пункт меню...'
)


# клавиатура для выбора коллекции
async def collections(mode: str = "default"):
    all_collections = await get_collections()
    keyboard = InlineKeyboardBuilder()
    for collection in all_collections:
        if mode == "photo":
            cb_data = f"photo_collection_{collection.id}"
        else:
            cb_data = f"collection_{collection.id}"

        keyboard.add(InlineKeyboardButton(text=collection.name, callback_data=cb_data))

    keyboard.add(InlineKeyboardButton(text='⬅️ Главное меню', callback_data='to_main_menu'))
    return keyboard.adjust(1).as_markup()


# клавиатура для выбора картин в коллекции
async def paintings(category_id):
    all_paintings = await get_collection_painting(category_id)

    if not all_paintings:
        return "Картины в данной коллекции не найдены.", None

    text_lines = ["🎨 <b>Картины в коллекции:</b>\n"]
    for painting in all_paintings:
        
        text_lines.append(
            f"• <a href='https://t.me/culture_for_everyone_bot?start=painting_{painting.id}'>{painting.name}</a>"
        )

    text = "\n".join(text_lines)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='⬅️ Коллекции', callback_data='to_all_collections')]
        ]
    )

    return text, keyboard