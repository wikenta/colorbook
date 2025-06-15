from scripts.dpi import get_pdf_dpi, get_standart_dpi
from scripts.converter import pdf_to_images
from scripts.rename_pages import rename_files
import os

folder = "pdf/parse"
folder_save = "pdf"
for filename in os.listdir(folder):
    if filename.endswith('.pdf'):
        pdf_path = os.path.join(folder, filename)

        # Получаем DPI изображений
        dpi = get_pdf_dpi(pdf_path)
        # Получаем стандартный DPI для изображений 
        standart_dpi = get_standart_dpi(dpi)

        # Конвертируем PDF в изображения
        output_dir = os.path.join(folder_save, f"{filename[:-4]} - {standart_dpi} DPI")
        print(f"Конвертируем {pdf_path} с DPI = {standart_dpi}")
        pdf_to_images(pdf_path, output_dir, standart_dpi)

        cover_folder = os.path.join(output_dir, "covers")
        os.makedirs(cover_folder, exist_ok=True)
        pages_folder = os.path.join(output_dir, "pages")
        os.makedirs(pages_folder, exist_ok=True)
        solutions_folder = os.path.join(output_dir, "solutions")
        os.makedirs(solutions_folder, exist_ok=True)
        
        # делаем паузу, чтобы пользователь раскидал страницы по папкам
        #input("Раскиньте страницы по папкам и нажмите Enter для продолжения...")

        # переименуем все файлы в covers, pages и solutions
        #rename_files(cover_folder, "cover")
        #rename_files(pages_folder, "page")
        #rename_files(solutions_folder, "solution")        

print("Готово!!!")