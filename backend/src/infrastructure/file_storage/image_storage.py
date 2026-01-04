import os
from pathlib import Path
from typing import Optional
import uuid


class ImageStorageService:
    """Service for storing and retrieving exercise images."""

    def __init__(self, storage_path: str = "static/exercises"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)

    def save_image(self, file_content: bytes, filename: Optional[str] = None) -> str:
        """
        Save image file and return the relative path.

        Args:
            file_content: Image file content as bytes
            filename: Optional original filename

        Returns:
            Relative path to saved image
        """
        # Generate unique filename
        if filename:
            ext = Path(filename).suffix
        else:
            ext = ".jpg"
        unique_filename = f"{uuid.uuid4()}{ext}"
        file_path = self.storage_path / unique_filename

        # Save file
        file_path.write_bytes(file_content)

        # Return relative path
        return str(file_path.relative_to("static"))

    def delete_image(self, image_path: str) -> None:
        """
        Delete image file.

        Args:
            image_path: Relative path to image (from static directory)
        """
        file_path = Path("static") / image_path
        if file_path.exists():
            file_path.unlink()

    def get_image_path(self, image_path: str) -> Optional[Path]:
        """
        Get full path to image file.

        Args:
            image_path: Relative path to image (from static directory)

        Returns:
            Full path to image file or None if not found
        """
        file_path = Path("static") / image_path
        if file_path.exists():
            return file_path
        return None





