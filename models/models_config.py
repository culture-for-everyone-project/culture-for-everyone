from pathlib import Path
from keras.models import load_model

BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"

MODEL_PATH_1 = MODELS_DIR / "model_1.h5"
MODEL_PATH_2 = MODELS_DIR / "model_2.h5"
MODEL_PATH_4 = MODELS_DIR / "model_4.keras"
MODEL_PATH_5 = MODELS_DIR / "model_5.h5"

model_1 = load_model(MODEL_PATH_1)
model_2 = load_model(MODEL_PATH_2)
model_4 = load_model(MODEL_PATH_4)
model_5 = load_model(MODEL_PATH_5)

MODELS = {
    1: model_1,
    2: model_2,
    4: model_4,
    5: model_5,
}
