from datetime import datetime

from pydantic import BaseModel, Field


class FileItemResponse(BaseModel):
    id: str = Field(..., description="Unique file identifier")
    filename: str = Field(..., description="Original filename")
    size: int = Field(..., description="File size in bytes", ge=0)
    created_at: datetime = Field(..., description="Upload timestamp")

    model_config = {"from_attributes": True}

class TaskRequest(BaseModel):
    """Request schema — fields the client must/can provide."""

    title: str = Field(..., title="Task Title", description="The title of the task",
                       min_length=3, max_length=50)

    description: str | None = Field(
        None, title="Task Description",
        description="The description of the task")

    completed: bool = Field(
        False,
        title="Task Completed",
        description="Whether the task is completed or not")

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Buy groceries",
                "description": "Milk, Bread, Eggs",
                "completed": False
            }
        }
    }


class TaskResponse(TaskRequest):
    """Response schema — extends TaskRequest with server-generated fields."""

    id: int

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "title": "Buy groceries",
                "description": "Milk, Bread, Eggs",
                "completed": False
            }
        }
    }
