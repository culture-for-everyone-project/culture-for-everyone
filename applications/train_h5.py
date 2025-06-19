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

# Директории
train_dir = pathlib.Path(DATASET_PATH)
val_dir = pathlib.Path(VALIDATION_DATASET_PATH)
test_dir = pathlib.Path(TEST_DATASET_PATH)

# Размер изображений
img_height = 224
img_width = 224

# Аугментация и генераторы
train_datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input,
    rotation_range=32,
    zoom_range=0.2,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    horizontal_flip=True,
    fill_mode="nearest"
)

val_datagen = ImageDataGenerator(preprocessing_function=preprocess_input)
test_datagen = ImageDataGenerator(preprocessing_function=preprocess_input)

# Генераторы данных
train = train_datagen.flow_from_directory(
    train_dir,
    target_size=(img_height, img_width),
    color_mode="rgb",
    class_mode="categorical",
    batch_size=32,
    shuffle=True,
    seed=123
)

# Словарь вида: {'501 яблоко': 0, '502 груша': 1, ...}
class_indices = train.class_indices

# Отсортируем по индексу, чтобы понять в каком порядке модель запомнила классы:
print("Классы датасета:")
for class_name, index in sorted(class_indices.items(), key=lambda x: x[1]):
    print(f"Класс {index}: {class_name}")


validation = val_datagen.flow_from_directory(
    val_dir,
    target_size=(img_height, img_width),
    color_mode="rgb",
    class_mode="categorical",
    batch_size=32,
    shuffle=True,
    seed=123
)

test = test_datagen.flow_from_directory(
    test_dir,
    target_size=(img_height, img_width),
    color_mode="rgb",
    class_mode="categorical",
    batch_size=32,
    shuffle=False
)

# Количество классов
num_classes = len(train.class_indices)

# Модель
base_model = MobileNetV2(
    input_shape=(img_height, img_width, 3),
    include_top=False,
    weights='imagenet',
    pooling='avg'
)
base_model.trainable = False

# Добавим классификатор
x = Dense(128, activation='relu')(base_model.output)
x = Dense(128, activation='relu')(x)
outputs = Dense(num_classes, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=outputs)

# Callbacks
early_stopping = EarlyStopping(
    monitor='val_loss',
    mode='min',
    patience=2,
    verbose=1,
    restore_best_weights=True,
)

checkpoint = ModelCheckpoint(
    'D:\\new\\models\\model_new_5.h5', # Путь к сохранению модели
    monitor='val_loss',
    mode='min',
    save_best_only=True
)

# Компиляция модели
model.compile(optimizer=Adam(learning_rate=0.0001),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Обучение
history = model.fit(
    train,
    validation_data=validation,
    epochs=20,
    callbacks=[early_stopping, checkpoint]
)


"""
# Отрисовка графика точности по эпохам
plt.plot(history.history['accuracy'], label='Train acc')
plt.plot(history.history['val_accuracy'], label='Val acc')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.title('Model Accuracy per Epoch')
plt.legend()
plt.grid(True)
plt.show()

# График функции потерь (loss)
plt.plot(history.history['loss'], label='Train loss')
plt.plot(history.history['val_loss'], label='Val loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Model Loss per Epoch')
plt.legend()
plt.grid(True)
plt.show()
"""

# Оценка
eval_loss, eval_accuracy = model.evaluate(test)
print(f"Evaluation accuracy: {eval_accuracy*100:.2f}%")

# Предсказания
pred_probs = model.predict(test)
pred = np.argmax(pred_probs, axis=1)

# Обратный словарь классов
labels = {v: k for k, v in train.class_indices.items()}
pred_labels = [labels[k] for k in pred]
true_labels = [labels[k] for k in test.classes]

# Accuracy
acc = accuracy_score(true_labels, pred_labels)
print(f'Accuracy on the test set: {100*acc:.2f}%')
