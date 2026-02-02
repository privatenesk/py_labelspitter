from sqlalchemy import Column, Integer, String, DateTime, JSON, Enum
from sqlalchemy.sql import func
import enum
from .database import Base

class JobStatus(str, enum.Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class PrintJob(Base):
    __tablename__ = "print_jobs"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    task_title = Column(String, index=True)
    category = Column(String)
    difficulty = Column(Integer)
    status = Column(String, default=JobStatus.PENDING) # stored as string to avoid enum issues in some DBs, can enforce in app
    job_metadata = Column(JSON, default={}) # Renamed to avoid confusion with sqlalchemy metadata

    def __repr__(self):
        return f"<PrintJob(id={self.id}, title='{self.task_title}', status='{self.status}')>"
