#создадим каталоги в облаке cloudinary
import cloudinary
import cloudinary.api
import cloudinary.uploader
from config.secret import CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET
from db_request.coloring.publisher import get_publishers
from db_request.coloring.series import get_root_series_by_publisher, get_child_series
from db_request.coloring.volume import get_books_by_publisher_without_series, get_books_by_series
from db_request.files.volume_cover_file import get_volume_cover_files, update_volume_cover_file_path
from db_request.files.volume_promo_file import create_volume_promo_file

cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET
)

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

        move_volume_files(book['id'], book_path)

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

        move_volume_files(book['id'], book_path)

def move_volume_files(book_id, new_folder):
    covers = get_volume_cover_files(book_id)
    for cover in covers:
        folder = cover['file_path'].rsplit('/', 1)[0]
        resources = cloudinary.api.resources(type="upload", prefix=folder + "/", max_results=500)
        for resource in resources.get('resources', []):
            public_id = resource['public_id']
            new_public_id = public_id.replace(folder, new_folder, 1)

            cloudinary.uploader.rename(public_id, new_public_id, overwrite=True)
            cloudinary.uploader.destroy(public_id)
            new_link = f"cloudinary://{new_public_id}"
            
            if cover['file_path'] == f"cloudinary://{public_id}":
                update_volume_cover_file_path(cover['id'], new_link)
            else:
                create_volume_promo_file(book_id, new_link)

create_publisher_folders()