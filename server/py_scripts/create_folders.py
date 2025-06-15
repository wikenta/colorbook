#создадим каталоги в облаке cloudinary
import asyncio
import cloudinary
import cloudinary.api
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
import re
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

def create_folder(path, name) -> str:
    """
    Создает папку в облаке Cloudinary по указанному пути.
    """
    try:
        cleaned = re.sub(r"[^\w\s\-.]", "", name)
        cleaned = cleaned.strip().replace(" ", "_")
        new_path = f"{path}/{cleaned}"
        cloudinary.api.create_folder(new_path)
        print(f"Created folder: {new_path}")
    except cloudinary.api.Error as e:
        if e.http_status == 409:  # Conflict error, folder already exists
            print(f"Folder already exists: {new_path}")
        else:
            print(f"Error creating folder {new_path}: {e}")
    return new_path

# корневые каталоги для издателей
async def create_publisher_folders():
    publishers = await get_publishers()
    for publisher in publishers:
        path = create_folder("", publisher['name_en'])

        await create_books_without_series_folders(publisher['id'], path)
        await create_root_series_folders(publisher['id'], path)

# вложенные каталоги для корневых серий
async def create_root_series_folders(publisher_id, path):
    root_series = await get_root_series_by_publisher(publisher_id)
    for series in root_series:
        new_path = create_folder(path, series['name_en'])

        await create_books_in_series_folders(series['id'], new_path)
        await create_series_folders(series['id'], new_path)

# каталоги для вложенных серий
async def create_series_folders(series_id, path):
    child_series = await get_child_series(series_id)
    for series in child_series:
        new_path = create_folder(path, series['name_en'])
        
        await create_books_in_series_folders(series['id'], new_path)
        await create_series_folders(series['id'], new_path)

# каталоги для книг без серии
async def create_books_without_series_folders(publisher_id, path):
    books = await get_books_by_publisher_without_series(publisher_id)
    for book in books:
        new_path = create_folder(path, book['name_en'])

        await move_volume_files(book['id'], new_path)

# каталоги для книг в серии
async def create_books_in_series_folders(series_id, path):
    books = await get_books_by_series(series_id)
    for book in books:
        new_path = create_folder(path, book['name_en'])

        await move_volume_files(book['id'], new_path)

async def move_volume_files(book_id, new_folder):
    covers = await get_volume_cover_files(book_id)
    print(f"Найдено {len(covers)} обложек для тома {new_folder}")
    for cover in covers:
        folder = cover['file_path'].rsplit('/', 1)[0]
        public_id = cover['file_path'].rsplit('/', 1)[-1].rsplit('.', 1)[0]
        resources = cloudinary.api.resources(type="upload", prefix=folder + "/", max_results=500)
        for resource in resources.get('resources', []):
            try:
                public_id = resource['public_id']
                link = f"https://res.cloudinary.com/{cloudinary.config().cloud_name}/image/upload/{public_id}"
                
                is_cover = cover['file_path'] == link
                file_extension = public_id.split('.')[-1]
                new_file_name = is_cover and "cover" or f"promo_{resource.get('number', 1)}"
                new_public_id = f"{new_folder}/{new_file_name}.{file_extension}"
                new_link = f"https://res.cloudinary.com/{cloudinary.config().cloud_name}/image/upload/{new_public_id}"

                print(f"Moving file {link}")
                print(f"To:         {new_link}")

                cloudinary.uploader.rename(public_id, new_public_id)
                print(f"File moved")
                
                if is_cover:
                    await update_volume_cover_file_path(cover['id'], new_link)
                    print(f"Cover file updated in database")
                else:
                    await create_volume_promo_file(book_id, new_link)
                    print(f"Promo file created in database")

                cloudinary.uploader.destroy(public_id)
                print(f"File deleted from old location")
            except cloudinary.api.Error as e:
                print(f"Error moving file {link}: {e}")

if __name__ == "__main__":
    asyncio.run(create_publisher_folders())