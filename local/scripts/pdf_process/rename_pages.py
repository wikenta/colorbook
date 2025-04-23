import os

def rename_files(folder: str, name: str, extension: str = '.png'):
    """
    Переименовывает изображения в папке
    """
    number = 0
    for filename in sorted(os.listdir(folder)):
        if not filename.startswith('{name}_') and filename.endswith(extension):
            number += 1
            new_filename = f'{name}_{number}{extension}'
            old_path = os.path.join(folder, filename)
            new_path = os.path.join(folder, new_filename)
            os.rename(old_path, new_path)