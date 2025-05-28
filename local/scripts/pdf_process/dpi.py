import fitz  # PyMuPDF

def get_pdf_dpi(pdf_path):
    max_dpi = 0
    doc = fitz.open(pdf_path)

    for i, page in enumerate(doc):
        print(f"Страница {i + 1:02}: ", end="")
        dpi = get_page_dpi(doc, page)
        max_dpi = max(max_dpi, dpi)
        print()

    print(f"Максимальное DPI файла: {max_dpi}")
    return int(max_dpi)

def get_page_dpi(doc, page):
    max_dpi = 0
    images = page.get_images(full=True)
    if not images:
        print(f"Нет встроенных изображений.")
        return max_dpi
    
    for img_index, img in enumerate(images):
        dpi = get_image_dpi(doc, page, img)
        print(f"{img_index + 1} - {dpi[0]:.0f}x{dpi[1]:.0f} DPI", end=", ")
        max_dpi = max(max_dpi, dpi[0], dpi[1])

    print(f"Максимальное DPI страницы: {max_dpi}")
    return int(max_dpi)

def get_image_dpi(doc, page, img):
    xref = img[0]  # XRef изображения
    pix = fitz.Pixmap(doc, xref)
    
    # Размеры в пикселях
    width_px = pix.width
    height_px = pix.height

    # Физический размер страницы в пунктах (1 пункт = 1/72 дюйма)
    rect = page.rect
    width_inches = rect.width / 72
    height_inches = rect.height / 72
    
    # Рассчитываем DPI
    dpi_x = width_px / width_inches
    dpi_y = height_px / height_inches

    return dpi_x, dpi_y

def get_standart_dpi(dpi):
    # округляем dpi до 50
    if dpi <= 50:
        return 50
    elif dpi <= 100:
        return 100
    elif dpi <= 150:
        return 150
    elif dpi <= 200:
        return 200
    elif dpi <= 300:
        return 300
    elif dpi <= 400:
        return 400
    elif dpi <= 600:
        return 600
    else:
        return 1200