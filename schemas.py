from datetime import datetime

from pydantic import BaseModel, Field


class FileItemResponse(BaseModel):
    id: str = Field(..., description="Unique file identifier")
    filename: str = Field(..., description="Original filename")
    size: int = Field(..., description="File size in bytes", ge=0)
    created_at: datetime = Field(..., description="Upload timestamp")
    bucket_id: int = Field(..., description="ID of the parent bucket")

    model_config = {"from_attributes": True}


class BucketCreate(BaseModel):
    name: str = Field(..., description="Unique bucket name", min_length=1)


class BucketResponse(BaseModel):
    id: int = Field(..., description="Bucket ID")
    name: str = Field(..., description="Bucket name")
    created_at: datetime = Field(..., description="Creation timestamp")

    model_config = {"from_attributes": True}


class BillingResponse(BaseModel):
    bucket_id: int
    bucket_name: str
    current_storage_bytes: int
    ingress_bytes: int
    egress_bytes: int
    internal_transfer_bytes: int
    count_write_requests: int
    count_read_requests: int

    model_config = {"from_attributes": True}

