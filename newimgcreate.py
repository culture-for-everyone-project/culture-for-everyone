import os
import random
from PIL import Image, ImageEnhance, ImageOps, ImageFilter

def generate_variations(input_folder, total_count=200):
    # Находим исходное изображение
    image_files = [f for f in os.listdir(input_folder) 
                  if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    if not image_files:
        print("Исходное изображение не найдено!")
        return
    
    original_path = os.path.join(input_folder, image_files[0])
    
    try:
        original_img = Image.open(original_path)
        width, height = original_img.size
        
        # Создаем 199 вариаций + оригинал = 200
        for i in range(1, total_count):
            # Создаем копию оригинала для преобразований
            variant = original_img.copy()
            
            # Применяем преобразования
            variant = apply_moderate_transformations(variant, width, height)
            
            # Сохраняем вариацию
            new_name = f"variant_{i}.jpg"
            variant.save(os.path.join(input_folder, new_name), quality=85)
            
        print(f"Готово! Создано {total_count} изображений в папке.")
        
    except Exception as e:
        print(f"Ошибка: {str(e)}")

def apply_moderate_transformations(img, original_w, original_h):
    """Применяет умеренные преобразования, сохраняя основное содержание"""
    
    # 1. Случайная яркость (80-120%)
    img = ImageEnhance.Brightness(img).enhance(random.uniform(0.8, 1.2))
    
    # 2. Случайный контраст (80-120%)
    img = ImageEnhance.Contrast(img).enhance(random.uniform(0.8, 1.2))
    
    # 3. Легкая резкость (50% chance)
    if random.random() < 0.5:
        img = img.filter(ImageFilter.SHARPEN)
    
    # 4. Зеркальное отражение (30% chance)
    if random.random() < 0.3:
        img = ImageOps.mirror(img)
    
    # 5. Умеренная обрезка (максимум 20% с каждой стороны)
    if random.random() < 0.7:  # 70% chance обрезки
        crop_percent = random.uniform(0.05, 0.2)  # От 5% до 20%
        left = random.randint(0, int(original_w * crop_percent))
        top = random.randint(0, int(original_h * crop_percent))
        right = original_w - random.randint(0, int(original_w * crop_percent))
        bottom = original_h - random.randint(0, int(original_h * crop_percent))
        img = img.crop((left, top, right, bottom))
    
    # 6. Небольшой поворот (максимум 10 градусов)
    if random.random() < 0.4:  # 40% chance
        angle = random.uniform(-10, 10)
        img = img.rotate(angle, expand=True, fillcolor='white')
    
    # 7. Легкое изменение цветовой температуры
    if random.random() < 0.3:
        r, g, b = img.split()
        r = r.point(lambda i: i * random.uniform(0.9, 1.1))
        b = b.point(lambda i: i * random.uniform(0.9, 1.1))
        img = Image.merge('RGB', (r, g, b))
    
    return img

# Укажите путь к папке с изображением
folder_path = r"C:\Users\Ксения\Desktop\dataset avangard 10-20\1 the girl in the chair"
generate_variations(folder_path, total_count=200)