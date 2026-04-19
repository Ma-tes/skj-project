from uuid import uuid4

from fastapi import APIRouter, Depends, Header, HTTPException, UploadFile
from fastapi.responses import FileResponse as FastAPIFileResponse
from sqlalchemy.orm import Session

from database import get_db
from models import Bucket, File
from repository import BucketRepository, FileRepository
from schemas import BillingResponse, BucketCreate, BucketResponse, FileItemResponse

router = APIRouter()


# --- Bucket endpoints ---

@router.post("/buckets/", status_code=201, response_model=BucketResponse)
def create_bucket(body: BucketCreate, db: Session = Depends(get_db)):
    repo = BucketRepository(db)
    if repo.get_by_name(body.name):
        raise HTTPException(status_code=409, detail="Bucket already exists")
    bucket = Bucket(name=body.name)
    return repo.create(bucket)


@router.get("/buckets/{bucket_id}/objects/", response_model=list[FileItemResponse])
def list_bucket_objects(bucket_id: int, db: Session = Depends(get_db)):
    bucket_repo = BucketRepository(db)
    bucket = bucket_repo.get_by_id(bucket_id)
    if not bucket:
        raise HTTPException(status_code=404, detail="Bucket not found")
    bucket.count_write_requests += 1
    db.commit()
    return bucket_repo.get_objects(bucket_id)


@router.get("/buckets/{bucket_id}/billing/", response_model=BillingResponse)
def get_bucket_billing(bucket_id: int, db: Session = Depends(get_db)):
    bucket_repo = BucketRepository(db)
    bucket = bucket_repo.get_by_id(bucket_id)
    if not bucket:
        raise HTTPException(status_code=404, detail="Bucket not found")
    return BillingResponse(
        bucket_id=bucket.id,
        bucket_name=bucket.name,
        current_storage_bytes=bucket.current_storage_bytes,
        ingress_bytes=bucket.ingress_bytes,
        egress_bytes=bucket.egress_bytes,
        internal_transfer_bytes=bucket.internal_transfer_bytes,
        count_write_requests=bucket.count_write_requests,
        count_read_requests=bucket.count_read_requests,
    )


# --- File endpoints ---

@router.get("/files/", response_model=list[FileItemResponse])
def list_files(user_id: str = Header(), db: Session = Depends(get_db)):
    repo = FileRepository(db)
    return repo.get_all(user_id)


@router.post("/files/upload", status_code=201, response_model=FileItemResponse)
def upload_file(
    file: UploadFile,
    bucket_id: int = Header(),
    user_id: str = Header(),
    x_internal_source: str | None = Header(default=None),
    db: Session = Depends(get_db),
):
    bucket_repo = BucketRepository(db)
    bucket = bucket_repo.get_by_id(bucket_id)
    if not bucket:
        raise HTTPException(status_code=404, detail="Bucket not found")

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
        bucket_id=bucket_id,
    )

    repo.create(db_file)

    is_internal = x_internal_source and x_internal_source.lower() == "true"
    bucket.current_storage_bytes += len(content)
    if is_internal:
        bucket.internal_transfer_bytes += len(content)
    else:
        bucket.ingress_bytes += len(content)
    bucket.count_write_requests += 1
    db.commit()

    return db_file


@router.get("/files/{file_id}")
def download_file(
    file_id: str,
    user_id: str = Header(),
    x_internal_source: str | None = Header(default=None),
    db: Session = Depends(get_db),
):
    repo = FileRepository(db)
    db_file = repo.get_by_id(file_id)

    if db_file is None or db_file.user_id != user_id or db_file.is_deleted:
        raise HTTPException(status_code=404, detail="File not found")

    is_internal = x_internal_source and x_internal_source.lower() == "true"
    bucket = db_file.bucket
    if is_internal:
        bucket.internal_transfer_bytes += db_file.size
    else:
        bucket.egress_bytes += db_file.size
    bucket.count_read_requests += 1
    db.commit()

    return FastAPIFileResponse(path=db_file.path, filename=db_file.filename)


@router.delete("/files/{file_id}", status_code=204)
def delete_file(file_id: str, user_id: str = Header(), db: Session = Depends(get_db)):
    repo = FileRepository(db)
    db_file = repo.get_by_id(file_id)

    if db_file is None or db_file.user_id != user_id or db_file.is_deleted:
        raise HTTPException(status_code=404, detail="File not found")

    bucket = db_file.bucket
    bucket.current_storage_bytes -= db_file.size
    bucket.count_write_requests += 1
    repo.soft_delete(db_file)
