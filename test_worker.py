import os
import sys
import time
import threading

sys.path.append(os.getcwd())

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.src.core.database import Base
from backend.src.core.models import PrintJob, JobStatus
from backend.src.worker.queue_manager import job_queue

# Setup Test DB (File based to share across threads reliably in test)
TEST_DB_FILE = "test_worker.db"
if os.path.exists(TEST_DB_FILE):
    os.remove(TEST_DB_FILE)

SQLALCHEMY_DATABASE_URL = f"sqlite:///{TEST_DB_FILE}"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Patch SessionLocal in queue_manager
import backend.src.worker.queue_manager
backend.src.worker.queue_manager.SessionLocal = TestingSessionLocal

def test_worker_flow():
    try:
        # Create tables
        Base.metadata.create_all(bind=engine)

        # Start Worker
        job_queue.start()

        # Create a Job in DB
        db = TestingSessionLocal()
        job = PrintJob(
            task_title="Worker Test",
            category="Test",
            difficulty=3,
            status=JobStatus.PENDING
        )
        db.add(job)
        db.commit()
        db.refresh(job)
        job_id = job.id
        db.close()

        # Enqueue
        job_queue.enqueue_job(job_id)

        # Wait for processing
        print("Waiting for worker...")
        time.sleep(2) # Give it time

        # Check status
        db = TestingSessionLocal()
        updated_job = db.query(PrintJob).filter(PrintJob.id == job_id).first()
        print(f"Job Status: {updated_job.status}")

        assert updated_job.status == JobStatus.COMPLETED

    finally:
        # Cleanup
        job_queue.stop()
        if os.path.exists(TEST_DB_FILE):
            os.remove(TEST_DB_FILE)
        print("Verification Successful!")

if __name__ == "__main__":
    test_worker_flow()
