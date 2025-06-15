import os
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

def apply_filters(input_path, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    # Получаем список всех файлов в папке
    for filename in os.listdir(input_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            img_path = os.path.join(input_path, filename)
            original = Image.open(img_path)
            filters = [
                ("noise", add_noise(original)),
                ("brightness_high", adjust_brightness(original, 1.5)),
                ("brightness_low", adjust_brightness(original, 0.5)),
                ("grayscale", convert_grayscale(original)),
                ("contrast", adjust_contrast(original, 1.5)),
                ("blur", apply_blur(original)),
                ("sharpness", adjust_sharpness(original, 2.0)),
                ("color", adjust_color(original, 1.5)),
                ("sepia", apply_sepia(original)) 
                ("red", apply_color_tone(original, (255, 100, 100))),
                ("yellow", apply_color_tone(original, (255, 255, 100))),
                ("green", apply_color_tone(original, (100, 255, 100))),
                ("cyan", apply_color_tone(original, (100, 255, 255))),
                ("blue", apply_color_tone(original, (100, 100, 255))),
                ("purple", apply_color_tone(original, (200, 100, 255)))
            ]
            
            # Сохраняем все варианты
            base_name = os.path.splitext(filename)[0]
            for filter_name, filtered_img in filters:
                output_filename = f"{base_name}_{filter_name}.jpg"
                output_filepath = os.path.join(output_path, output_filename)
                filtered_img.save(output_filepath, "JPEG")

def add_noise(image):
    """Добавляет шум к изображению"""
    img_array = np.array(image)
    noise = np.random.randint(-50, 50, img_array.shape, dtype=np.int32)
    noisy_img = np.clip(img_array + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(noisy_img)

def adjust_brightness(image, factor):
    """Изменяет яркость изображения"""
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)

def convert_grayscale(image):
    """Конвертирует в черно-белое"""
    return image.convert("L")

def adjust_contrast(image, factor):
    """Изменяет контраст изображения"""
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)

def apply_blur(image):
    """Добавляет размытие к изображению"""
    return image.filter(ImageFilter.BLUR)

def adjust_sharpness(image, factor):
    """Изменяет резкость изображения"""
    enhancer = ImageEnhance.Sharpness(image)
    return enhancer.enhance(factor)

def adjust_color(image, factor):
    """Изменяет насыщенность цветов"""
    enhancer = ImageEnhance.Color(image)
    return enhancer.enhance(factor)

def detect_edges(image):
    """Обнаруживает границы на изображении"""
    return image.filter(ImageFilter.FIND_EDGES)

def apply_sepia(image):
    """Применяет сепию к изображению"""
    width, height = image.size
    pixels = image.load()
    
    for py in range(height):
        for px in range(width):
            r, g, b = image.getpixel((px, py))
            
            tr = int(0.393 * r + 0.769 * g + 0.189 * b)
            tg = int(0.349 * r + 0.686 * g + 0.168 * b)
            tb = int(0.272 * r + 0.534 * g + 0.131 * b)
            
            pixels[px, py] = (min(255, tr), min(255, tg), min(255, tb))
    
    return image
    
def apply_color_tone(image, tone_color):
    """Применяет цветовой оттенок к изображению"""
    img_array = np.array(image)
    if len(img_array.shape) == 2:
        img_array = np.stack((img_array,)*3, axis=-1)
    normalized = img_array.astype(np.float32) / 255.0
    tone = np.array(tone_color, dtype=np.float32) / 255.0
    tone_filter = np.ones_like(normalized) * tone
    tinted = (normalized * 0.7 + tone_filter * 0.3)
    tinted = np.clip(tinted * 255, 0, 255).astype(np.uint8)
    return Image.fromarray(tinted)

if __name__ == "__main__":
    input_folder = r"input_files\70"  
    output_folder = "Portrait_of_Platon_Alexandrovich_Zubov".replace(' ','_')  
    
    apply_filters(input_folder, output_folder)
    print("Обработка изображений завершена!")
