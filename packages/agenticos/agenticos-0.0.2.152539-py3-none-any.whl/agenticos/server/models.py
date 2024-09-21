from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class NodeDescription(BaseModel):
    name: str
    description: str
    inputs: dict[str, str]


class Task(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    inputs: dict[str, str]
    status: TaskStatus
    output: str
