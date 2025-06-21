import pathlib
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from keras.layers import Dense
from keras.models import Model
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras_preprocessing.image import ImageDataGenerator
from keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input
from keras.optimizers import Adam
from sklearn.metrics import accuracy_score
from configuration import DATASET_PATH, TEST_DATASET_PATH, VALIDATION_DATASET_PATH

# Директории с данными для обучения, валидации и теста
train_dir = pathlib.Path(DATASET_PATH)
val_dir = pathlib.Path(VALIDATION_DATASET_PATH)
test_dir = pathlib.Path(TEST_DATASET_PATH)

# Размеры изображений, к которым будут приводиться входные данные
img_height = 224
img_width = 224

# Создание генератора данных с аугментацией для обучения
train_datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input,  # предобработка под MobileNetV2
    rotation_range=32,       # случайные повороты изображений в диапазоне ±32 градуса
    zoom_range=0.2,          # случайное приближение/удаление на 20%
    width_shift_range=0.2,   # случайное смещение по ширине на 20%
    height_shift_range=0.2,  # случайное смещение по высоте на 20%
    shear_range=0.2,         # сдвиг углов
    horizontal_flip=True,    # случайное зеркальное отражение
    fill_mode="nearest",     # способ заполнения новых пикселей после трансформаций
)

# Для валидации и теста используется только предобработка без аугментаций
val_datagen = ImageDataGenerator(preprocessing_function=preprocess_input)
test_datagen = ImageDataGenerator(preprocessing_function=preprocess_input)

# Генераторы, которые будут читать изображения из папок, автоматически формируя батчи
train = train_datagen.flow_from_directory(
    train_dir,
    target_size=(img_height, img_width),  # все изображения к одному размеру
    color_mode="rgb",
    class_mode="categorical",  # многоклассовая классификация
    batch_size=32,
    shuffle=True,  # перемешать данные для обучения
    seed=123,      # зафиксировать генератор случайных чисел для воспроизводимости
)

# Словарь: название класса -> индекс
class_indices = train.class_indices

# Вывод отсортированного по индексу списка классов, чтобы понимать порядок, в котором модель их "видит"
print("Классы датасета:")
for class_name, index in sorted(class_indices.items(), key=lambda x: x[1]):
    print(f"Класс {index}: {class_name}")

# Такой же генератор для валидации (без аугментаций)
validation = val_datagen.flow_from_directory(
    val_dir,
    target_size=(img_height, img_width),
    color_mode="rgb",
    class_mode="categorical",
    batch_size=32,
    shuffle=True,
    seed=123,
)

# Генератор для тестовой выборки, без перемешивания, чтобы корректно сопоставить метки
test = test_datagen.flow_from_directory(
    test_dir,
    target_size=(img_height, img_width),
    color_mode="rgb",
    class_mode="categorical",
    batch_size=32,
    shuffle=False,
)

# Определение количество классов для последнего слоя модели
num_classes = len(train.class_indices)

# Загрузка базовой предобученной модели MobileNetV2 без классификатора (include_top=False)
# Используются предварительно обученные веса с ImageNet
base_model = MobileNetV2(
    input_shape=(img_height, img_width, 3),
    include_top=False,
    weights='imagenet',
    pooling='avg',  # глобальное среднее пуллирование для получения вектора признаков
)

# Базовая модель заморожена, чтобы ее веса не обновлялись во время обучения
base_model.trainable = False

# Новый классификатор поверх базовой модели:
# два полносвязных слоя с ReLU и выходной слой с softmax на число классов
x = Dense(128, activation='relu')(base_model.output)
x = Dense(128, activation='relu')(x)
outputs = Dense(num_classes, activation='softmax')(x)

# Итоговая модель Keras
model = Model(inputs=base_model.input, outputs=outputs)

# Коллбеки для контроля обучения

# Ранняя остановка, если валидационная потеря не улучшается в течение 2 эпох
early_stopping = EarlyStopping(
    monitor='val_loss',
    mode='min',
    patience=2,
    verbose=1,
    restore_best_weights=True,
)

# Сохраняется лучшая модель по показателю val_loss
checkpoint = ModelCheckpoint(
    '___',  # Здесь нужно указать путь для сохранения модели
    monitor='val_loss',
    mode='min',
    save_best_only=True,
)

# Компиляция модели с оптимизатором Adam и функцией потерь categorical_crossentropy для многоклассовой классификации
model.compile(
    optimizer=Adam(learning_rate=0.0001),
    loss='categorical_crossentropy',
    metrics=['accuracy'],
)

# Запуск обучение модели на тренировочных данных с валидацией
history = model.fit(
    train,
    validation_data=validation,
    epochs=20,
    callbacks=[early_stopping, checkpoint],
)


"""
# Ниже закомментирован код для отрисовки графиков точности и функции потерь по эпохам

plt.plot(history.history['accuracy'], label='Train acc')
plt.plot(history.history['val_accuracy'], label='Val acc')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.title('Model Accuracy per Epoch')
plt.legend()
plt.grid(True)
plt.show()

plt.plot(history.history['loss'], label='Train loss')
plt.plot(history.history['val_loss'], label='Val loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Model Loss per Epoch')
plt.legend()
plt.grid(True)
plt.show()
"""

# Оценка модели на тестовой выборке, вывод точности
eval_loss, eval_accuracy = model.evaluate(test)
print(f"Evaluation accuracy: {eval_accuracy * 100:.2f}%")

# Предсказания вероятностей для теста
pred_probs = model.predict(test)

# Получаем индексы классов с максимальной вероятностью
pred = np.argmax(pred_probs, axis=1)

# Обратный словарь: индекс -> название класса
labels = {v: k for k, v in train.class_indices.items()}

# Преобразование индексов предсказаний и истинных меток в названия классов
pred_labels = [labels[k] for k in pred]
true_labels = [labels[k] for k in test.classes]

# Рассчёт точности классификации на тестовой выборке с помощью sklearn
acc = accuracy_score(true_labels, pred_labels)
print(f'Accuracy on the test set: {100 * acc:.2f}%')
