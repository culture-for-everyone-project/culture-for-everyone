from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import CommandStart, Command

from aiogram.filters import StateFilter=
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
import app.database.requests as rq

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer('Здравствуйте! Пожалуйста, пришлите название картины или её фотографию.', reply_markup=kb.main_keyboard)

# Обработчик команды /help
@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("Пока никакой помощи.")


# Обработчик команды /audio
@router.message(Command("audio"))
async def cmd_help(message: Message):
    await message.answer("🎧|Все аудиолекции доступны по ссылке: https://izo.t2.ru/museum/14")

@router.message(F.text == 'Помощь')
async def catalog(message: Message):
    await message.answer('Пока никакой помощи.', reply_markup=kb.main_keyboard)

@router.message(F.text == 'Язык')
async def catalog(message: Message):
    await message.answer('Only russian', reply_markup=kb.main_keyboard)

@router.message(F.text == 'Дополнительные источники информации')
async def catalog(message: Message):
    await message.answer('Википедия: https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0', reply_markup=kb.main_keyboard)



@router.message(F.text == 'Коллекции и доступные картины музея')
async def catalog(message: Message):
    await message.answer('Выберите коллекцию музея.', reply_markup=await kb.collections())


@router.callback_query(F.data.startswith('collection_'))
async def collection(callback: CallbackQuery):
    await callback.answer('Вы выбрали коллекцию.')
    await callback.message.answer('Выберите картину.',
                                  reply_markup=await kb.paintings(callback.data.split('_')[1]))



@router.callback_query(F.data.startswith('painting_'))
async def collection(callback: CallbackQuery):
    painting_id = callback.data.split('_')[1]
    painting_data = await rq.get_painting(painting_id)

    await callback.answer('Вы выбрали картину.')
    await callback.message.answer_photo(
        painting_data.image_url,  
        caption=f'<b><i>{painting_data.name}</i></b>\n\n'
                f'<i>{painting_data.author}</i>\n'
                f'<i>{painting_data.year}</i>\n\n'
                f'<blockquote>{painting_data.description}</blockquote>',
        parse_mode="HTML"
    )
"""
то же самое, но отправляется ссылка на изображение и прогружается его превью.
@router.callback_query(F.data.startswith('painting_'))
async def collection(callback: CallbackQuery):
    painting_id = callback.data.split('_')[1]
    painting_data = await rq.get_painting(painting_id)

    await callback.answer('Вы выбрали картину.')
    await callback.message.answer(
        f'{painting_data.image_url}\n\n'
        f'<b><i>{painting_data.name}</i></b>\n\n'
        f'<i>{painting_data.author}</i>\n'
        f'<i>{painting_data.year}</i>\n\n'
        f'<blockquote>{painting_data.description}</blockquote>',
        parse_mode="HTML"
    )
"""

@router.message(F.text == 'Отправить название картины')
async def ask_painting_name(message: Message, state: FSMContext):
    await message.answer(
        'Отправьте название картины.', 
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state("waiting_for_painting_name")

@router.message(StateFilter("waiting_for_painting_name"))
async def painting_name_sent(message: Message, state: FSMContext):
    painting_name = message.text
    painting_data = await rq.get_painting_by_name(painting_name)
        
    if painting_data:
        await message.answer_photo(
            painting_data.image_url,  
            caption=f'<b><i>{painting_data.name}</i></b>\n\n'
                f'<i>{painting_data.author}</i>\n'
                f'<i>{painting_data.year}</i>\n\n'
                f'<blockquote>{painting_data.description}</blockquote>\n\n'
                f'<i>{painting_data.material}</i>\n'
                f'<i>{painting_data.size}</i>',
            parse_mode="HTML",
            reply_markup=kb.main_keyboard
        )
    else:
        await message.answer(
            "К сожалению, информации об этой картине нет.", 
            reply_markup=kb.main_keyboard
        )
    await state.clear()

@router.callback_query(F.data == 'to_main_menu')
async def to_main_menu_handler(callback: CallbackQuery):
    await callback.message.answer("Вы в главном меню.", reply_markup= kb.main_keyboard)
    await callback.answer()

@router.callback_query(F.data == 'to_all_collections')
async def to_main_menu_handler(callback: CallbackQuery):
    await callback.message.answer("Выбор коллекции музея.", reply_markup= await kb.collections())
    await callback.answer()
