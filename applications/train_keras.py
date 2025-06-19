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

# Пути к директориям
train_dir = pathlib.Path(DATASET_PATH)
val_dir = pathlib.Path(VALIDATION_DATASET_PATH)
test_dir = pathlib.Path(TEST_DATASET_PATH)

# Параметры изображения
img_height = 224
img_width = 224
batch_size = 32


data_augmentation = keras.Sequential([
    layers.RandomRotation(0.2),
    layers.RandomZoom(0.3),
    layers.RandomTranslation(0.2, 0.2),
    layers.RandomFlip("horizontal_and_vertical"),
    layers.RandomContrast(0.3),
    layers.RandomBrightness(0.2)
])



def prepare_dataset(directory, shuffle=False, augment=False):
    """Функция для загрузки и предобработки данных"""
    # Сначала получаем генератор для сохранения class_names
    gen = keras.utils.image_dataset_from_directory(
        directory,
        image_size=(img_height, img_width),
        batch_size=batch_size,
        shuffle=shuffle,
        label_mode='categorical'
    )
    
    # Сохраняем имена классов
    class_names = gen.class_names
    
    # Создаем dataset
    ds = keras.utils.image_dataset_from_directory(
        directory,
        image_size=(img_height, img_width),
        batch_size=batch_size,
        shuffle=shuffle,
        label_mode='categorical'
    )
    
    # Предобработка и аугментация
    def preprocess(image, label):
        image = preprocess_input(image)
        if augment:
            image = data_augmentation(image)
        return image, label
    
    return (
        ds.map(preprocess, num_parallel_calls=tf.data.AUTOTUNE)
           .prefetch(tf.data.AUTOTUNE),
        class_names
    )

# Загрузка данных с сохранением имен классов
train_ds, train_class_names = prepare_dataset(train_dir, shuffle=True, augment=True)
val_ds, _ = prepare_dataset(val_dir, shuffle=True)
test_ds, _ = prepare_dataset(test_dir)

# Создаем правильное соответствие классов
label_map = {i: name for i, name in enumerate(train_class_names)}
num_classes = len(train_class_names)

print("Правильный порядок классов:")
for i, name in label_map.items():
    print(f"{i}: {name}")

#НОВОЕ
# Создание модели
base_model = MobileNetV2(
    input_shape=(img_height, img_width, 3),
    include_top=False,
    weights='imagenet',
    pooling='avg'
)


# Создание модели
base_model = MobileNetV2(
    input_shape=(img_height, img_width, 3),
    include_top=False,
    weights='imagenet',
    pooling='avg'
)
base_model.trainable = False

inputs = keras.Input(shape=(img_height, img_width, 3))
x = base_model(inputs, training=False)
x = layers.Dense(128, activation='relu')(x)
x = layers.Dense(128, activation='relu')(x)
outputs = layers.Dense(num_classes, activation='softmax')(x)

model = keras.Model(inputs, outputs)

# Колбэки (без save_format)
callbacks = [
    keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True), #patience = 2 по умолчанию кол во эпох для ранней останвки обучения
    keras.callbacks.ModelCheckpoint(
        'model_mobilenetv2.keras',
        save_best_only=True,
        monitor='val_loss'
    )
]

# Компиляция модели
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)


# Обучение модели
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=20,
    callbacks=callbacks
)

# Оценка модели
eval_loss, eval_accuracy = model.evaluate(test_ds)
print(f"Evaluation accuracy: {eval_accuracy*100:.2f}%")

# Предсказания
pred = model.predict(test_ds)
pred_classes = np.argmax(pred, axis=1)

# Получаем истинные метки
true_classes = np.concatenate([y.numpy().argmax(axis=1) for x, y in test_ds], axis=0)

# Преобразуем индексы в имена классов
true_labels = [label_map[i] for i in true_classes]
pred_labels = [label_map[i] for i in pred_classes]

# Оценка точности
acc = accuracy_score(true_labels, pred_labels)
print(f"Accuracy on the test set: {acc*100:.2f}%")

# Сохраняем соответствие классов
with open('class_indices.json', 'w') as f:
    json.dump(label_map, f, indent=4)
