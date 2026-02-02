import os
import sys

# Add project root to path
sys.path.append(os.getcwd())

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.src.core.database import Base
from backend.src.core.models import PrintJob, JobStatus

# Use SQLite in-memory for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_create_and_read_job():
    # Create tables
    Base.metadata.create_all(bind=engine)

    # Create session
    db = TestingSessionLocal()

    # Create a job
    new_job = PrintJob(
        task_title="Test Task",
        category="Testing",
        difficulty=5,
        status=JobStatus.PENDING.value,
        job_metadata={"test": "data"}
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    print(f"Created Job: {new_job}")

    # Read back
    job = db.query(PrintJob).filter(PrintJob.id == new_job.id).first()
    assert job is not None
    assert job.task_title == "Test Task"
    assert job.difficulty == 5
    assert job.job_metadata["test"] == "data"
    print("Verification Successful!")

if __name__ == "__main__":
    test_create_and_read_job()
