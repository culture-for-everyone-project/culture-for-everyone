import logging
import os
import bot.keyboards as kb
import database.db_requests as rq
from aiogram import Bot, F, Router
from aiogram.filters import CommandStart, Command, StateFilter, CommandObject
from aiogram.enums import ContentType
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from bot.predictions import predict_class


router = Router()


# =====================================================================================================================================
# COMMANDS
# =====================================================================================================================================


# /start_bot
@router.message(Command('start_bot'))
async def cmd_start_bot(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer("Здравствуйте! Выберите действие:", 
                         reply_markup=kb.main_keyboard)


# /add_info
@router.message(Command("add_info"))
async def cmd_add_info(message: Message):
    await message.answer("🌐|Официальный сайт «Эрмитаж-Урал»: https://i-z-o.art/constitutor/centr-ermitazh-ural/\n🎧|Все аудиолекции доступны по ссылке: https://izo.t2.ru/museum/14")


# =====================================================================================================================================
# MAIN MENU - 1 [НАЙТИ КАРТИНУ ПО КОЛЛЕКЦИИ МУЗЕЯ]
# =====================================================================================================================================


@router.message(CommandStart(deep_link=True))
async def handle_deep_link_start(message: Message, command: CommandObject):
    if command.args and command.args.startswith("painting_"):
        painting_id = command.args.split("_")[1]
        painting_data = await rq.get_painting_by_id(painting_id)

        if painting_data:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(
                    text='⬅️ Найти другие картины в каталоге',
                    callback_data=f'collection_{painting_data.collection_id}'
                )]]
            )


            caption = (
                f'<b><i>{painting_data.name}</i></b>\n\n'
                f'<i>{painting_data.author}</i>\n'
                f'<i>{painting_data.year}</i>\n'
                f'<i>{painting_data.material}</i>\n'
                f'<i>{painting_data.size}</i>\n\n'
                f'<i>{painting_data.image_page_link}</i>'
            )

            await message.answer_photo(
                photo=painting_data.image,
                caption=caption,
                parse_mode="HTML"
            )

            if painting_data.audio:
                await message.answer_audio(
                    audio=painting_data.audio,
                    caption=f'Все аудиолекции доступны по ссылке: {painting_data.audio_page_link}\n'
                )

            await message.answer(
                f'<blockquote>{painting_data.description}</blockquote>',
                parse_mode="HTML",
                reply_markup=keyboard
            )
        else:
            await message.answer("Картина не найдена в базе данных.", reply_markup=kb.main_keyboard)
    else:
        await message.answer("Привет! Выберите действие:", reply_markup=kb.main_keyboard)


@router.message(F.text == 'Найти картину по коллекции музея')
async def catalog(message: Message):
    await message.answer('Выберите коллекцию музея:', 
                         reply_markup=await kb.collections())


@router.callback_query(F.data.startswith('collection_'))
async def collection(callback: CallbackQuery):
    await callback.answer('Вы выбрали коллекцию.')

    collection_id = int(callback.data.split('_')[1])
    text, keyboard = await kb.paintings(collection_id)

    await callback.message.answer(
        text,
        reply_markup=keyboard,
        parse_mode="HTML",
        disable_web_page_preview=True 
    )


@router.callback_query(F.data == 'to_main_menu')
async def to_main_menu_handler(callback: CallbackQuery):
    await callback.message.answer("Вы в главном меню.", 
                                  reply_markup= kb.main_keyboard)
    await callback.answer()


@router.callback_query(F.data == 'to_all_collections')
async def to_main_menu_handler(callback: CallbackQuery):
    await callback.message.answer("Выбор коллекции музея.", 
                                  reply_markup= await kb.collections())
    await callback.answer()


# =====================================================================================================================================
# MAIN MENU - 2 [НАЙТИ КАРТИНУ ПО НАЗВАНИЮ]
# =====================================================================================================================================


@router.message(F.text == 'Найти картину по названию')
async def ask_painting_name(message: Message, state: FSMContext):
    await message.answer('🖼️ Теперь отправьте название картины.',
        reply_markup=kb.main_keyboard,
        callback_data='search_by_name'
    )
    await state.set_state("waiting_for_painting_name")


@router.message(StateFilter("waiting_for_painting_name"), F.content_type == ContentType.TEXT)
async def painting_name_sent(message: Message, state: FSMContext):
    painting_name = message.text.strip()
    painting_ids = await rq.get_painting_ids_by_name(painting_name)

    if painting_ids:
        for painting_id in painting_ids:
            painting_data = await rq.get_painting_by_id(painting_id)

            if painting_data:
                keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[[InlineKeyboardButton(
                        text='⬅️ Найти другие картины по названию',
                        callback_data='to_search_by_name'
                    )]]
                )

                caption = (
                    f'<b><i>{painting_data.name}</i></b>\n\n'
                    f'<i>{painting_data.author}</i>\n'
                    f'<i>{painting_data.year}</i>\n'
                    f'<i>{painting_data.material}</i>\n'
                    f'<i>{painting_data.size}</i>\n\n'
                    f'<i>{painting_data.image_page_link}</i>'
                )

                await message.answer_photo(
                    photo=painting_data.image,
                    caption=caption,
                    parse_mode="HTML"
                )

                if painting_data.audio:
                    await message.answer_audio(
                        audio=painting_data.audio,
                        caption=f'Все аудиолекции доступны по ссылке: {painting_data.audio_page_link}\n'
                    )

                await message.answer(
                    f'<blockquote>{painting_data.description}</blockquote>',
                    parse_mode="HTML",
                    reply_markup=keyboard
                )
            else:
                await message.answer("Одна из картин не найдена в базе.")
    else:
        await message.answer("К сожалению, картина с таким названием не найдена.",
                             reply_markup=kb.main_keyboard)

    await state.clear()


@router.callback_query(F.data == 'to_search_by_name')
async def back_to_search_by_name(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "🖼️ Теперь отправьте название картины.",
    )
    await state.set_state("waiting_for_new_painting_name")
    await callback.answer()


@router.message(StateFilter("waiting_for_new_painting_name"), F.content_type == ContentType.TEXT)
async def painting_name_sent(message: Message, state: FSMContext):
    painting_name = message.text.strip()
    painting_ids = await rq.get_painting_ids_by_name(painting_name)

    if painting_ids:
        for painting_id in painting_ids:
            painting_data = await rq.get_painting_by_id(painting_id)

            if painting_data:
                keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[[InlineKeyboardButton(
                        text='⬅️ Найти другие картины по названию',
                        callback_data='to_search_by_name'
                    )]]
                )

                caption = (
                    f'<b><i>{painting_data.name}</i></b>\n\n'
                    f'<i>{painting_data.author}</i>\n'
                    f'<i>{painting_data.year}</i>\n'
                    f'<i>{painting_data.material}</i>\n'
                    f'<i>{painting_data.size}</i>\n\n'
                    f'<i>{painting_data.image_page_link}</i>'
                )

                await message.answer_photo(
                    photo=painting_data.image,
                    caption=caption,
                    parse_mode="HTML"
                )

                if painting_data.audio:
                    await message.answer_audio(
                        audio=painting_data.audio,
                        caption=f'Все аудиолекции доступны по ссылке: {painting_data.audio_page_link}\n'
                    )

                await message.answer(
                    f'<blockquote>{painting_data.description}</blockquote>',
                    parse_mode="HTML",
                    reply_markup=keyboard
                )
            else:
                await message.answer("Одна из картин не найдена в базе.")
    else:
        await message.answer("К сожалению, картина с таким названием не найдена.",
                             reply_markup=kb.main_keyboard)

    await state.clear()


# =====================================================================================================================================
# MAIN MENU - 3 [НАЙТИ КАРТИНУ ПО ФОТОГРАФИИ]
# =====================================================================================================================================


# FSM-состояния
class PhotoSearchState(StatesGroup):
    choosing_collection = State()
    waiting_for_photo = State()


@router.message(F.text == 'Найти картину по фотографии')
async def ask_collection_for_photo_search(message: Message, state: FSMContext):
    await message.answer('Выберите коллекцию для поиска:',
                         reply_markup=await kb.collections(mode="photo"))  
    await state.set_state(PhotoSearchState.choosing_collection)


@router.callback_query(F.data.startswith('photo_collection_'), StateFilter(PhotoSearchState.choosing_collection))
async def collection_chosen_for_photo(callback: CallbackQuery, state: FSMContext):
    collection_id = int(callback.data.split('_')[2])  # теперь индекс 2
    await state.update_data(collection_id=collection_id)

    await callback.message.answer('📷 Теперь отправьте фотографию картины.')
    await state.set_state(PhotoSearchState.waiting_for_photo)
    await callback.answer()


# Обработка фото
@router.message(StateFilter(PhotoSearchState.waiting_for_photo), F.content_type == ContentType.PHOTO)
async def handle_photo_with_collection(message: Message, state: FSMContext, bot: Bot):
    file_path = None
    try:
        user_data = await state.get_data()
        collection_id = user_data.get("collection_id")
        print(f"Получена коллекция: {collection_id}")

        photo = message.photo[-1]
        file = await bot.get_file(photo.file_id)
        file_path = f"temp_{message.from_user.id}.jpg"
        await bot.download_file(file.file_path, destination=file_path)

        print(f"Файл загружен: {file_path}")

        # Предсказание и поиск
        painting_prediction_name = predict_class(file_path, collection_id) 
        print(f"Распознанная картина: {painting_prediction_name}")
        painting_id = await rq.get_painting_id_by_prediction(painting_prediction_name)

        if painting_id:
            painting_data = await rq.get_painting_by_id(painting_id)
            if painting_data:
                keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[[InlineKeyboardButton(
                        text='⬅️ Найти другую картину по фотографии',
                        callback_data='to_search_by_photo'
                    )]]
                )

                caption = (
                    f'<b><i>{painting_data.name}</i></b>\n\n'
                    f'<i>{painting_data.author}</i>\n'
                    f'<i>{painting_data.year}</i>\n'
                    f'<i>{painting_data.material}</i>\n'
                    f'<i>{painting_data.size}</i>\n\n'
                    f'<i>{painting_data.image_page_link}</i>'
                )

                await message.answer_photo(
                    photo=painting_data.image,
                    caption=caption,
                    parse_mode="HTML"
                )

                if painting_data.audio:
                    await message.answer_audio(
                        audio=painting_data.audio,
                        caption=f'Все аудиолекции доступны по ссылке: {painting_data.audio_page_link}\n'
                    )

                await message.answer(
                    f'<blockquote>{painting_data.description}</blockquote>',
                    parse_mode="HTML",
                    reply_markup=keyboard
                )
            else:
                await message.answer("Картину найти не удалось в базе.", reply_markup=kb.main_keyboard)
        else:
            await message.answer("Картина не распознана.", reply_markup=kb.main_keyboard)

    except Exception as e:
        logging.error(f"Ошибка: {e}")
        await message.answer("Ошибка при обработке изображения.", reply_markup=kb.main_keyboard)

    finally:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)

        await state.clear()


# Обработка кнопки "Найти другую картину по фотографии"
@router.callback_query(F.data == 'to_search_by_photo')
async def to_photo_search_again(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Выберите коллекцию для поиска:',
                                   reply_markup=await kb.collections(mode="photo")) 
    await state.set_state(PhotoSearchState.choosing_collection)
    await callback.answer()


# =====================================================================================================================================
