from uuid import uuid4

from fastapi import APIRouter, Depends, Header, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from database import get_db
from models import File
from repository import FileRepository

router = APIRouter(prefix="/files")

@router.get("/")
def list_files(user_id: str = Header(), db: Session = Depends(get_db)):
    repo = FileRepository(db)
    files = repo.get_all(user_id)

    return [
        {
            "id": f.id,
            "filename": f.filename,
            "size": f.size,
            "created_at": f.created_at,
        }
        for f in files
    ]


@router.post("/upload", status_code=201)
def upload_file(file: UploadFile, user_id: str = Header(), db: Session = Depends(get_db)):
    repo = FileRepository(db)
    file_id = str(uuid4())

    content = file.file.read()
    path = repo.save_to_disk(user_id, file_id, content)

    db_file = File(
        id=file_id,
        user_id=user_id,
        filename=file.filename,
        path=path,
        size=len(content),
    )

    repo.create(db_file)
    return {"id": db_file.id, "filename": db_file.filename, "size": db_file.size}


@router.get("/{file_id}")
def download_file(file_id: str, user_id: str = Header(), db: Session = Depends(get_db)):
    repo = FileRepository(db)
    db_file = repo.get_by_id(file_id)

    if db_file is None or db_file.user_id != user_id:
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path=db_file.path, filename=db_file.filename)


@router.delete("/{file_id}", status_code=204)
def delete_file(file_id: str, user_id: str = Header(), db: Session = Depends(get_db)):
    repo = FileRepository(db)
    db_file = repo.get_by_id(file_id)

    if db_file is None or db_file.user_id != user_id:
        raise HTTPException(status_code=404, detail="File not found")
    repo.delete(db_file)
