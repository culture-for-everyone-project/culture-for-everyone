import os
import shutil
import zipfile
import numpy as np
import pandas as pd
from PIL import Image, ImageEnhance, ImageFilter
from tqdm import tqdm


class OtechDatasetCreator:
    def __init__(self, source_dir, output_dir="Russian art of the 20th century"):
        self.source_dir = source_dir
        self.output_dir = output_dir
        self.metadata = []
        self.augmentation_types = [
            'brightness', 'contrast', 'rotation',
            'flip', 'color_shift', 'blur',
            'sharpness', 'noise', 'sepia'
        ]

    def apply_specific_augmentation(self, img, augmentation_type):
        if augmentation_type == 'brightness':
            enhancer = ImageEnhance.Brightness(img)
            return enhancer.enhance(np.random.uniform(0.7, 1.5))
        elif augmentation_type == 'contrast':
            enhancer = ImageEnhance.Contrast(img)
            return enhancer.enhance(np.random.uniform(0.7, 1.5))
        elif augmentation_type == 'rotation':
            return img.rotate(np.random.uniform(-15, 15))
        elif augmentation_type == 'flip':
            if np.random.rand() > 0.5:
                return img.transpose(Image.FLIP_LEFT_RIGHT)
            return img.transpose(Image.FLIP_TOP_BOTTOM)
        elif augmentation_type == 'color_shift':
            enhancer = ImageEnhance.Color(img)
            return enhancer.enhance(np.random.uniform(0.5, 1.5))
        elif augmentation_type == 'blur':
            return img.filter(ImageFilter.GaussianBlur(radius=np.random.uniform(0.5, 1.5)))
        elif augmentation_type == 'sharpness':
            enhancer = ImageEnhance.Sharpness(img)
            return enhancer.enhance(np.random.uniform(0.5, 3.0))
        elif augmentation_type == 'noise':
            arr = np.array(img)
            noise = np.random.randint(-50, 50, arr.shape, dtype=np.int32)
            arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
            return Image.fromarray(arr)
        elif augmentation_type == 'sepia':
            sepia_filter = np.array([
                [0.393, 0.769, 0.189],
                [0.349, 0.686, 0.168],
                [0.272, 0.534, 0.131]
            ])
            arr = np.array(img).dot(sepia_filter.T)
            return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
        return img

    def create_variation(self, img, variation_type):
        img_variant = img.copy()

        if variation_type == 1:
            # Вариация 1: Яркость + Контраст + Поворот
            img_variant = self.apply_specific_augmentation(img_variant, 'brightness')
            img_variant = self.apply_specific_augmentation(img_variant, 'contrast')
            img_variant = self.apply_specific_augmentation(img_variant, 'rotation')
        elif variation_type == 2:
            # Вариация 2: Цветовой сдвиг + Размытие + Шум
            img_variant = self.apply_specific_augmentation(img_variant, 'color_shift')
            img_variant = self.apply_specific_augmentation(img_variant, 'blur')
            img_variant = self.apply_specific_augmentation(img_variant, 'noise')
        elif variation_type == 3:
            # Вариация 3: Отражение + Резкость + Сепия
            img_variant = self.apply_specific_augmentation(img_variant, 'flip')
            img_variant = self.apply_specific_augmentation(img_variant, 'sharpness')
            img_variant = self.apply_specific_augmentation(img_variant, 'sepia')
        elif variation_type == 4:
            # Вариация 4: Комбинация всех преобразований с умеренными параметрами
            for aug in self.augmentation_types:
                img_variant = self.apply_specific_augmentation(img_variant, aug)

        return img_variant

    def process_icon(self, icon_name, icon_files):
        icon_dir = os.path.join(self.output_dir, icon_name.lower().replace(" ", "_"))
        os.makedirs(icon_dir, exist_ok=True)

        for i, img_path in enumerate(icon_files, 1):
            try:
                img = Image.open(img_path)
                if img.mode != 'RGB':
                    img = img.convert('RGB')

                original_path = os.path.join(icon_dir, f"original_{i}.jpg")
                img.save(original_path, quality=95)

                for variant in range(1, 5):
                    img_variant = self.create_variation(img, variant)
                    variant_path = os.path.join(icon_dir, f"variant_{i}_{variant}.jpg")
                    img_variant.save(variant_path, quality=90)

            except Exception as e:
                print(f"Ошибка обработки {img_path}: {str(e)}")

    def create_zip(self):
        """Создаёт zip-архив датасета"""
        zip_path = f"{self.output_dir}.zip"
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(self.output_dir):
                for file in files:
                    zipf.write(
                        os.path.join(root, file),
                        arcname=os.path.relpath(os.path.join(root, file), self.output_dir)
                    )
        return zip_path

    def process_collection(self):
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)

        os.makedirs(self.output_dir)

        for icon_dir in os.listdir(self.source_dir):
            if not os.path.isdir(os.path.join(self.source_dir, icon_dir)):
                continue

            icon_name = icon_dir.replace("_", " ").title()
            icon_files = [
                os.path.join(self.source_dir, icon_dir, f)
                for f in os.listdir(os.path.join(self.source_dir, icon_dir))
                if f.lower().endswith(('.jpg', '.jpeg', '.png'))
            ]

            print(f"Обработка: {icon_name} ({len(icon_files)} изображений)")
            self.process_icon(icon_name, icon_files)

        pd.DataFrame(self.metadata).to_csv(
            os.path.join(self.output_dir, "metadata.csv"),
            index=False
        )

        zip_path = self.create_zip()
        print(f"Датасет создан: {zip_path}")
        print("\n" + "=" * 50)
        print("ПРОВЕРКА СТРУКТУРЫ ПЕРЕД АРХИВАЦИЕЙ")
        print("=" * 50)

        if not os.path.exists(self.output_dir):
            print(f"ОШИБКА: Папка {self.output_dir} не создана!")
        else:
            print(f"Папка {self.output_dir} существует.")

            for root, dirs, files in os.walk(self.output_dir):
                print(f"\nПапка: {os.path.relpath(root, self.output_dir)}")

                if not files and not dirs:
                    print("  → [папка пуста]")
                else:
                    for file in files[:10]:
                        print(f"  → Файл: {file}")
                    if len(files) > 10:
                        print(f"  → ... и ещё {len(files) - 10} файлов")

        print("\n" + "=" * 50)


if __name__ == "__main__":
    SOURCE_DIR = r"C:\Users\Илья\Documents\domestic_art"
    print(f"Проверяемая папка: {SOURCE_DIR}")

    creator = OtechDatasetCreator(SOURCE_DIR)
    creator.process_collection()