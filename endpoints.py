from uuid import uuid4

import models
from fastapi import APIRouter, Depends, Header, HTTPException, UploadFile
from fastapi.responses import FileResponse as FastAPIFileResponse
from sqlalchemy.orm import Session

from database import get_db
from models import File
from repository import FileRepository
from schemas import FileItemResponse, TaskRequest, TaskResponse

router = APIRouter(prefix="/files")

@router.get("/", response_model=list[FileItemResponse])
def list_files(user_id: str = Header(), db: Session = Depends(get_db)):
    repo = FileRepository(db)
    return repo.get_all(user_id)

@router.post("/upload", status_code=201, response_model=FileItemResponse)
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
    return db_file

@router.get("/{file_id}")
def download_file(file_id: str, user_id: str = Header(), db: Session = Depends(get_db)):
    repo = FileRepository(db)
    db_file = repo.get_by_id(file_id)

    if db_file is None or db_file.user_id != user_id:
        raise HTTPException(status_code=404, detail="File not found")
    return FastAPIFileResponse(path=db_file.path, filename=db_file.filename)

@router.delete("/{file_id}", status_code=204)
def delete_file(file_id: str, user_id: str = Header(), db: Session = Depends(get_db)):
    repo = FileRepository(db)
    db_file = repo.get_by_id(file_id)

    if db_file is None or db_file.user_id != user_id:
        raise HTTPException(status_code=404, detail="File not found")
    repo.delete(db_file)

task_router = APIRouter(prefix="/db-tasks", tags=["db-tasks"])

@task_router.post("/", response_model=TaskResponse,
                  summary="Create a new task in the database",
                  response_description="The created task",
                  status_code=201)
def create_db_task(task: TaskRequest, db: Session = Depends(get_db)):
    db_task = models.Task(title=task.title, description=task.description, completed=task.completed)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@task_router.get("/", response_model=list[TaskResponse],
                 summary="Get all tasks from the database",
                 response_description="List of all tasks")
def get_db_tasks(db: Session = Depends(get_db)):
    return db.query(models.Task).all()
