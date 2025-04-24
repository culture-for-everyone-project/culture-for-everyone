import pathlib
import numpy as np
import tensorflow as tf
from sklearn.metrics import accuracy_score

from keras.api.models import Model
from keras.api.layers import Dense
from keras.api.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
from keras.src.legacy.preprocessing.image import ImageDataGenerator
from keras.api.applications import MobileNetV2
from keras.api.applications import mobilenet_v2

from config import DATASET_PATH, TEST_DATASET_PATH, VALIDATION_DATASET_PATH



# Пути к директориям
train_dir = pathlib.Path(DATASET_PATH)
val_dir = pathlib.Path(VALIDATION_DATASET_PATH)
test_dir = pathlib.Path(TEST_DATASET_PATH)

# Параметры
img_height = 224
img_width = 224
batch_size = 32

# Предобработка и аугментация
train_datagen = ImageDataGenerator(
    preprocessing_function=mobilenet_v2.preprocess_input,
    rotation_range=32,
    zoom_range=0.2,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    horizontal_flip=True,
    fill_mode="nearest"
)

test_datagen = ImageDataGenerator(preprocessing_function=mobilenet_v2.preprocess_input)

# Загрузка данных
train = train_datagen.flow_from_directory(
    train_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical',
    shuffle=True,
    seed=123
)

val = train_datagen.flow_from_directory(
    val_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical',
    shuffle=True,
    seed=123
)

test = test_datagen.flow_from_directory(
    test_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical',
    shuffle=False
)

# Количество классов
num_classes = len(train.class_indices)

# Создание модели
base_model = MobileNetV2(
    input_shape=(img_height, img_width, 3),
    include_top=False,
    weights='imagenet',
    pooling='avg'
)
base_model.trainable = False

x = Dense(128, activation='relu')(base_model.output)
x = Dense(128, activation='relu')(x)
output = Dense(num_classes, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=output)

# Колбэки
callbacks = [
    EarlyStopping(monitor='val_loss', patience=2, restore_best_weights=True, verbose=1),
    ModelCheckpoint('fruit224mobile.h5', save_best_only=True, monitor='val_loss', mode='min', verbose=1)
]

# Компиляция модели
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Обучение модели
history = model.fit(
    train,
    validation_data=val,
    epochs=20,
    callbacks=callbacks
)

# Оценка модели
eval_loss, eval_accuracy = model.evaluate(test)
print(f"Evaluation accuracy: {eval_accuracy*100:.2f}%")

# Предсказания
pred = model.predict(test)
pred_classes = np.argmax(pred, axis=1)

# Преобразование индексов в имена классов
label_map = {v: k for k, v in train.class_indices.items()}
true_classes = test.classes
true_labels = [label_map[i] for i in true_classes]
pred_labels = [label_map[i] for i in pred_classes]

# Оценка точности
acc = accuracy_score(true_labels, pred_labels)
print(f"Accuracy on the test set: {acc*100:.2f}%")
