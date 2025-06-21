import pathlib
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras import layers, models
from keras.applications import MobileNetV2
from keras.applications.mobilenet_v2 import preprocess_input
from sklearn.metrics import accuracy_score
from applications.configuration import DATASET_PATH, TEST_DATASET_PATH, VALIDATION_DATASET_PATH
import json

# Директории с данными для обучения, валидации и теста
train_dir = pathlib.Path(DATASET_PATH)
val_dir = pathlib.Path(VALIDATION_DATASET_PATH)
test_dir = pathlib.Path(TEST_DATASET_PATH)

# Размеры входных изображений 
img_height = 224
img_width = 224
batch_size = 32  # размер батча для загрузки данных

# Последовательность слоев для аугментации данных — случайные преобразования изображений
data_augmentation = keras.Sequential(
    [
        layers.RandomRotation(0.2),             # случайный поворот до 20% (±0.2 радиан)
        layers.RandomZoom(0.3),                 # случайное приближение/удаление до 30%
        layers.RandomTranslation(0.2, 0.2),     # случайный сдвиг по горизонтали и вертикали до 20%
        layers.RandomFlip("horizontal_and_vertical"),  # случайное зеркальное отражение по обеим осям
        layers.RandomContrast(0.3),             # случайное изменение контраста до 30%
        layers.RandomBrightness(0.2),           # случайное изменение яркости до 20%
    ]
)

def prepare_dataset(directory, shuffle=False, augment=False):
    """
    Функция для загрузки и подготовки датасета из директории.
    Аргументы:
        directory: pathlib.Path - путь к папке с изображениями по классам
        shuffle: bool - перемешивать ли данные
        augment: bool - применять ли аугментацию (только для train)
    Возвращает:
        ds: tf.data.Dataset - готовый к обучению датасет с предобработкой и опциональной аугментацией
        class_names: список строк с названиями классов
    """
    # Генератор для получения списка классов
    gen = keras.utils.image_dataset_from_directory(
        directory,
        image_size=(img_height, img_width),  # привести изображения к единому размеру
        batch_size=batch_size,
        shuffle=shuffle,
        label_mode="categorical",            # метки в one-hot формате
    )
    class_names = gen.class_names  # список имен классов

    # Основной датасет (также из той же директории с параметрами)
    ds = keras.utils.image_dataset_from_directory(
        directory,
        image_size=(img_height, img_width),
        batch_size=batch_size,
        shuffle=shuffle,
        label_mode="categorical",
    )

    # Функция предобработки и аугментации для каждого батча
    def preprocess(image, label):
        image = preprocess_input(image)  # предобработка под MobileNetV2 (нормализация)
        if augment:                     # если аугментация разрешена
            image = data_augmentation(image)  # случайные преобразования
        return image, label

    # prefetch для ускорения загрузки данных
    return (
        ds.map(preprocess, num_parallel_calls=tf.data.AUTOTUNE).prefetch(tf.data.AUTOTUNE),
        class_names,
    )

# Загрузка датасетов
# Для train включена аугментация и перемешивание
train_ds, train_class_names = prepare_dataset(train_dir, shuffle=True, augment=True)
# Для валидации аугментация отключена, перемешивание включено
val_ds, _ = prepare_dataset(val_dir, shuffle=True)
# Для теста аугментация и перемешивание отключены (чтобы сохранить порядок)
test_ds, _ = prepare_dataset(test_dir)

# Словарь, сопоставляющий индексы классов их именам (0: "картина1")
label_map = {i: name for i, name in enumerate(train_class_names)}
num_classes = len(train_class_names)  # число классов

# Вывод правильного порядока классов. важно для сопоставления меток
print("Правильный порядок классов:")
for i, name in label_map.items():
    print(f"{i}: {name}")

# Создание базовой модель MobileNetV2 без верхних слоев (классификатора),
# с предобученными весами на ImageNet, и глобальным средним пуллингом для выхода
base_model = MobileNetV2(
    input_shape=(img_height, img_width, 3),
    include_top=False,     # без классификатора ImageNet
    weights="imagenet",    # загрузка весов предобученной модели
    pooling="avg",         # лобальный средний пуллинг к выходу сверточных слоев
)
base_model.trainable = False  # базовая модель заморожена, чтобы не менять ее веса при обучении

# Входной слой с формой изображения
inputs = keras.Input(shape=(img_height, img_width, 3))

# Передача входа в базовую модель, режим training=False, чтобы отключить слой dropout/BN
x = base_model(inputs, training=False)

# Добавление двух полносвязных слоёв с активацией ReLU
x = layers.Dense(128, activation="relu")(x)
x = layers.Dense(128, activation="relu")(x)

# Выходной слой с числом нейронов, равным числу классов, с активацией softmax для вероятностей
outputs = layers.Dense(num_classes, activation="softmax")(x)

# Итоговая модель от входа до выхода
model = keras.Model(inputs, outputs)

# Колбэки для контроля процесса обучения:
callbacks = [
    # Ранняя остановка, если val_loss не улучшается 5 эпох подряд, при этом возвращаются лучшие веса
    keras.callbacks.EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True),
    # Сохраняется только лучшая модель по val_loss в файл KERAS
    keras.callbacks.ModelCheckpoint(
        "model_mobilenetv2.keras",
        save_best_only=True,
        monitor="val_loss",
    ),
]

# Компилzwbz моделb с оптимизатором Adam, функцией потерь categorical_crossentropy
# и метрикой accuracy (точность)
model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"],
)

# Обучение модели на тренировочном датасете, валидация на валидационном,
# с количеством эпох 20 и указанными колбэками
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=20,
    callbacks=callbacks,
)

# Оценка качества обученной модели на тестовом датасете
eval_loss, eval_accuracy = model.evaluate(test_ds)
print(f"Evaluation accuracy: {eval_accuracy * 100:.2f}%")

# Предсказания модели для теста (вероятности классов)
pred = model.predict(test_ds)

# Преобразование вероятности в индексы с максимальной вероятностью (выбор класса)
pred_classes = np.argmax(pred, axis=1)

# ИСТИННЫЕ МЕТКИ ИЗ ТЕСТОВОГО ДАТАСЕТА
# собираются все метки из батчей и берётся argmax по one-hot кодировке
true_classes = np.concatenate([y.numpy().argmax(axis=1) for x, y in test_ds], axis=0)

# Преобразование числовых индексов в имена классов
true_labels = [label_map[i] for i in true_classes]
pred_labels = [label_map[i] for i in pred_classes]

# Рассчёт точности классификации на тестовой выборке с помощью sklearn
acc = accuracy_score(true_labels, pred_labels)
print(f"Accuracy on the test set: {acc * 100:.2f}%")

# Сохраняется словарь соответствия классов в json
with open("class_indices.json", "w") as f:
    json.dump(label_map, f, indent=4)
