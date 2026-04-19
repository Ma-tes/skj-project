from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Bucket(Base):
    __tablename__ = "buckets"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    current_storage_bytes: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    ingress_bytes: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    egress_bytes: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    internal_transfer_bytes: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    count_write_requests: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    count_read_requests: Mapped[int] = mapped_column(Integer, default=0, server_default="0")

    files: Mapped[list["File"]] = relationship(back_populates="bucket")


class File(Base):
    __tablename__ = "files"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id: Mapped[str] = mapped_column(String, index=True)
    filename: Mapped[str] = mapped_column(String)
    path: Mapped[str] = mapped_column(String)
    size: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    bucket_id: Mapped[int] = mapped_column(ForeignKey("buckets.id"))
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")

    bucket: Mapped["Bucket"] = relationship(back_populates="files")

