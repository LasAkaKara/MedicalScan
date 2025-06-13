import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

def upload_avatar(file_path, public_id=None):
    result = cloudinary.uploader.upload(
        file_path,
        folder="avatars",
        public_id=public_id,
        overwrite=True,
        resource_type="image"
    )
    return result.get("secure_url")