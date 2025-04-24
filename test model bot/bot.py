import logging
import os
import numpy as np
import asyncio
import tensorflow as tf

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.enums import ContentType
from keras.api.models import load_model

from config import API_TOKEN, MODEL_PATH



# Логгинг
logging.basicConfig(level=logging.INFO)

# Токен и модель
BOT_TOKEN = API_TOKEN
model = load_model(MODEL_PATH)

class_labels = [
    "Девушка гадает на ромашке", "Поклоненине младенцу",
    "Бой быков", "Девочка в кресле", "Княжна Тараканова",
    "Крестьянка с детьми", "Портрет сестры, Анна Владимировна Розанова", "Витязь на распутье"
]

# Предобработка изображения
def get_img_array(img_path, size=(224, 224)):
    img = tf.keras.preprocessing.image.load_img(img_path, target_size=size)
    array = tf.keras.preprocessing.image.img_to_array(img)
    array = np.expand_dims(array, axis=0)
    return tf.keras.applications.mobilenet_v2.preprocess_input(array)

# Предсказание
def predict_class(img_path):
    try:
        img_array = get_img_array(img_path)
        prediction = model.predict(img_array)
        class_index = np.argmax(prediction)
        return class_labels[class_index]
    except Exception as e:
        logging.error(f"Ошибка предсказания: {e}")
        return "Не удалось распознать изображение."

# Создание бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Команда /start
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("Привет! Отправь фотографию картины")

# Команда /help
@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer("Просто отправь мне фотографию картины.")

# Обработка изображения
@dp.message(lambda message: message.content_type == ContentType.PHOTO)
async def handle_photo(message: types.Message, bot: Bot):
    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)
    file_path = f"temp_{message.from_user.id}.jpg"
    await bot.download_file(file.file_path, destination=file_path)

    result = predict_class(file_path)
    await message.answer(f"Название картины: {result}")
    os.remove(file_path)

# Запуск
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
