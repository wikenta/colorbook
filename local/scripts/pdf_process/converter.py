from pdf2image import convert_from_path
import os

# Функция для конвертации PDF в изображения
def pdf_to_images(input_pdf, output_dir, dpi=300):
    # Создаем папку, если её нет
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Конвертируем PDF в список изображений
    images = convert_from_path(input_pdf, dpi=dpi)

    # Сохраняем каждую страницу как изображение
    for i, image in enumerate(images):
        image_path = os.path.join(output_dir, f"page_{(i + 1):02}.png")
        print(f"Сохраняю страницу {i+1}: {image_path}")
        image.save(image_path, "PNG")

    print(f"Страницы сохранены как изображения в {output_dir}")
    # 