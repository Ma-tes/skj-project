import os
import shutil

from sqlalchemy.orm import Session

from models import File

STORAGE_DIR = "storage"

class FileRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, user_id: str) -> list[File]:
        return self.db.query(File).filter(File.user_id == user_id).all()

    def get_by_id(self, file_id: str) -> File | None:
        return self.db.query(File).filter(File.id == file_id).first()

    def create(self, file: File) -> File:
        self.db.add(file)
        self.db.commit()
        self.db.refresh(file)
        return file

    def delete(self, file: File) -> None:
        if os.path.exists(file.path):
            os.remove(file.path)
        self.db.delete(file)
        self.db.commit()

    @staticmethod
    def save_to_disk(user_id: str, file_id: str, content: bytes) -> str:
        user_dir = os.path.join(STORAGE_DIR, user_id)
        os.makedirs(user_dir, exist_ok=True)
        file_path = os.path.join(user_dir, file_id)
        with open(file_path, "wb") as f:
            f.write(content)
        return file_path
