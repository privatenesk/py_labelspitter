from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from backend.src.core.models import JobStatus

class JobConfig(BaseModel):
    fillers: Optional[str] = "default"
    scaling_factor: Optional[float] = 1.0

class JobCreate(BaseModel):
    task_title: str
    category: str
    difficulty: int = Field(..., ge=1, le=10)
    config: Optional[JobConfig] = None

class JobResponse(BaseModel):
    id: int
    created_at: datetime
    task_title: str
    category: str
    difficulty: int
    status: JobStatus
    job_metadata: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True
