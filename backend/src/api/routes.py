from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List

from backend.src.core.database import get_db
from backend.src.core.models import PrintJob, JobStatus
from backend.src.api.schemas import JobCreate, JobResponse
from backend.src.worker.queue_manager import job_queue

router = APIRouter()

@router.post("/jobs", response_model=JobResponse)
def create_job(job_in: JobCreate, db: Session = Depends(get_db)):
    # Create DB Entry
    job_metadata = {"config": job_in.config.dict()} if job_in.config else {}

    db_job = PrintJob(
        task_title=job_in.task_title,
        category=job_in.category,
        difficulty=job_in.difficulty,
        status=JobStatus.PENDING,
        job_metadata=job_metadata
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)

    # Enqueue
    job_queue.enqueue_job(db_job.id)

    return db_job

@router.get("/jobs", response_model=List[JobResponse])
def get_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    jobs = db.query(PrintJob).order_by(PrintJob.created_at.desc()).offset(skip).limit(limit).all()
    return jobs

@router.get("/jobs/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(PrintJob).filter(PrintJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
