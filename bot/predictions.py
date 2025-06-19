import logging
import numpy as np
import tensorflow as tf
from models.models_config import MODELS
from models.class_labels import CLASS_LABELS


logging.basicConfig(level=logging.INFO)


def get_img_array(img_path, size=(224, 224)):
    img = tf.keras.preprocessing.image.load_img(img_path, target_size=size)
    array = tf.keras.preprocessing.image.img_to_array(img)
    array = np.expand_dims(array, axis=0)
    return tf.keras.applications.mobilenet_v2.preprocess_input(array)


def predict_class(img_path: str, collection_id: int):
    try:
        img_array = get_img_array(img_path)
        model = MODELS.get(collection_id)
        if model is None:
            logging.error(f"Модель для коллекции {collection_id} не найдена.")
            return "Не удалось распознать изображение."
        prediction = model.predict(img_array) # 
        class_index = np.argmax(prediction)
        class_label = CLASS_LABELS.get(collection_id)
        if class_label is None:
            logging.error(f"Метки классов для коллекции {collection_id} не найдены.")
            return "Не удалось распознать изображение."
        painting_class_label = class_label[class_index]
        return painting_class_label
    except Exception as e:
        logging.error(f"Ошибка предсказания: {e}")
        return "Не удалось распознать изображение."
