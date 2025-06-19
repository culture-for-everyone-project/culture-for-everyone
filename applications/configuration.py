from pathlib import Path

# Корень проекта
BASE_DIR = Path(__file__).resolve().parent.parent

BOT_TOKEN = 'Токен бота'

# Пути к моделям
MODEL_PATH_1 = BASE_DIR / 'models' / 'model_1.h5'
MODEL_PATH_2 = BASE_DIR / 'models' / 'model_2.h5'
MODEL_PATH_4 = BASE_DIR / 'models' / 'model_4.keras'
MODEL_PATH_5 = BASE_DIR / 'models' / 'model_5.h5'

# Пути к датасетам
DATASET_PATH = BASE_DIR / 'datasets' / '№ датасета' / 'ds_№'
VALIDATION_DATASET_PATH = BASE_DIR / 'datasets' / '№ датасета' / 'ds_№_validation'
TEST_DATASET_PATH = BASE_DIR / 'datasets' / '№ датасета' / 'ds_№_test'

# Путь к БД
DB_PATH = BASE_DIR / 'db.sqlite3'
