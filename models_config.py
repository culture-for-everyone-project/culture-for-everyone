from keras.models import load_model

MODEL_PATH_1 = "D:\\new\\models\\model_1.h5"
MODEL_PATH_2 = "D:\\new\\models\\model_2.h5"
MODEL_PATH_4 = "D:\\new\\models\\model_4.keras"
MODEL_PATH_5 = "D:\\new\\models\\model_5.h5"

model_1 = load_model(MODEL_PATH_1)
model_2 = load_model(MODEL_PATH_2)
model_4 = load_model(MODEL_PATH_4)
model_5 = load_model(MODEL_PATH_5)

MODELS= {
    1: model_1,
    2: model_2,
    4: model_4,
    5: model_5
}