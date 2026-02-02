import threading
import queue
import time
import traceback
from sqlalchemy.orm import Session
from backend.src.core.database import SessionLocal
from backend.src.core.models import PrintJob, JobStatus
from backend.src.logic.label_generator import LabelGenerator
from backend.src.interfaces.printer import PrinterInterface, MockPrinter

class JobQueue:
    def __init__(self):
        self.queue = queue.Queue()
        self.printer: PrinterInterface = MockPrinter() # Default to Mock
        self.generator = LabelGenerator()
        self.running = False
        self.thread = None

    def start(self):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._worker_loop, daemon=True)
        self.thread.start()
        print("Worker thread started.")

    def stop(self):
        self.running = False
        self.queue.put(None) # Sentinel
        if self.thread:
            self.thread.join()
            print("Worker thread stopped.")

    def enqueue_job(self, job_id: int):
        self.queue.put(job_id)
        print(f"Job {job_id} enqueued.")

    def _worker_loop(self):
        print("Worker loop running...")
        while self.running:
            try:
                job_id = self.queue.get(timeout=1.0)
            except queue.Empty:
                continue

            if job_id is None:
                break

            self._process_job(job_id)
            self.queue.task_done()

    def _process_job(self, job_id: int):
        db: Session = SessionLocal()
        try:
            job = db.query(PrintJob).filter(PrintJob.id == job_id).first()
            if not job:
                print(f"Job {job_id} not found in DB.")
                return

            print(f"Processing Job {job_id}: {job.task_title}")
            job.status = JobStatus.PROCESSING
            db.commit()

            # Generate
            try:
                image = self.generator.generate(
                    title=job.task_title,
                    category=job.category,
                    difficulty=job.difficulty,
                    options=job.job_metadata.get("config") if job.job_metadata else None
                )

                # Print
                self.printer.print_image(image)

                job.status = JobStatus.COMPLETED
            except Exception as e:
                print(f"Error processing job {job_id}: {e}")
                traceback.print_exc()
                job.status = JobStatus.FAILED
                # Maybe store error in metadata?

            db.commit()

        except Exception as e:
            print(f"Critical worker error: {e}")
        finally:
            db.close()

# Singleton instance
job_queue = JobQueue()
