from keras.models import load_model
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

BOT_TOKEN = '7623605344:AAEPY67yvCqcLCLolAMTGOQzW9RPBljlK3w'

DB_PATH = BASE_DIR / 'db.sqlite3'

MODEL_PATH_1 = BASE_DIR / 'models' / 'model_1.h5'
MODEL_PATH_2 = BASE_DIR / 'models' / 'model_2.h5'
MODEL_PATH_4 = BASE_DIR / 'models' / 'model_4.keras'
MODEL_PATH_5 = BASE_DIR / 'models' / 'model_5.h5'

DATASET_PATH = BASE_DIR / 'datasets' / '4' / 'ds_5'
VALIDATION_DATASET_PATH = BASE_DIR / 'datasets' / '4' / 'ds_5_validation'
TEST_DATASET_PATH = BASE_DIR / 'datasets' / '4' / 'ds_5_test'

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

COLLECTION_NAMES = {
    1: "Русский художественный авангард 1910-1920-х годов",
    2: "Западноевропейское искусство XIV-XIX веков",
    3: "Русская иконопись XVII - начала ХХ века",
    4: "Отечественное искусство XX века",
    5: "Русское искусство XVIII – начала XX века",
}
