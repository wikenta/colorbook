#создадим каталоги в облаке cloudinary
import cloudinary
import cloudinary.api
from config.secret import CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET
from db_request.publisher import get_publishers
from db_request.series import get_root_series_by_publisher, get_child_series
from db_request.volume import get_books_by_publisher_without_series, get_books_by_series

cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET
)

# переместим все каталоги в "ВСЕ_ЗДЕСЬ"
def move_all_folders_to_root():
    try:
        folders = cloudinary.api.sub_folders()
        for folder in folders['folders']:
            path = folder['path']
            if path != "ВСЕ_ЗДЕСЬ":
                new_path = f"ВСЕ_ЗДЕСЬ/{path}"
                cloudinary.api.move_folder(path, new_path)
                print(f"Moved folder {path} to {new_path}")
    except cloudinary.api.Error as e:
        print(f"Error moving folders: {e}")

# корневые каталоги для издателей
def create_publisher_folders():
    publishers = get_publishers()
    for publisher in publishers:
        try:
            path = f"{publisher['name_en']}"
            cloudinary.api.create_folder(path)
            print(f"Created folder for publisher: {path}")
        except cloudinary.api.Error as e:
            print(f"Error creating folder for publisher {path}: {e}")

        create_books_without_series_folders(publisher['id'], path)
        create_root_series_folders(publisher['id'], path)

# вложенные каталоги для корневых серий
def create_root_series_folders(publisher_id, path):
    root_series = get_root_series_by_publisher(publisher_id)
    for series in root_series:
        path = f"{path}/{series['name_en']}"
        try:
            cloudinary.api.create_folder(path)
            print(f"Created folder for series: {series['name_en']}")
        except cloudinary.api.Error as e:
            print(f"Error creating folder for series {series['name_en']}: {e}")

        create_books_in_series_folders(series['id'], path)
        create_series_folders(series['id'], path)

# каталоги для вложенных серий
def create_series_folders(series_id, path):
    child_series = get_child_series(series_id)
    for series in child_series:
        path = f"{path}/{series['name_en']}"
        try:
            cloudinary.api.create_folder(path)
            print(f"Created folder for series: {series['name_en']}")
        except cloudinary.api.Error as e:
            print(f"Error creating folder for series {series['name_en']}: {e}")
        
        create_books_in_series_folders(series['id'], path)
        create_series_folders(series['id'], path)

# каталоги для книг без серии
def create_books_without_series_folders(publisher_id, path):
    books = get_books_by_publisher_without_series(publisher_id)
    for book in books:
        book_path = f"{path}/{book['name_en']}"
        try:
            cloudinary.api.create_folder(book_path)
            print(f"Created folder for book without series: {book['name_en']}")
        except cloudinary.api.Error as e:
            print(f"Error creating folder for book {book['name_en']}: {e}")

# каталоги для книг в серии
def create_books_in_series_folders(series_id, path):
    books = get_books_by_series(series_id)
    for book in books:
        book_path = f"{path}/{book['name_en']}"
        try:
            cloudinary.api.create_folder(book_path)
            print(f"Created folder for book in series: {book['name_en']}")
        except cloudinary.api.Error as e:
            print(f"Error creating folder for book {book['name_en']}: {e}")

move_all_folders_to_root()
create_publisher_folders()