import os
import sys
import shutil
import time

sys.path.append(os.getcwd())

# 1. Setup Test DB
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

TEST_DB_FILE = "test_api.db"
if os.path.exists(TEST_DB_FILE):
    os.remove(TEST_DB_FILE)

SQLALCHEMY_DATABASE_URL = f"sqlite:///{TEST_DB_FILE}"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 2. Patch Database Session
import backend.src.core.database
backend.src.core.database.SessionLocal = TestingSessionLocal
backend.src.core.database.engine = engine

# Patch Queue Manager SessionLocal as well
import backend.src.worker.queue_manager
backend.src.worker.queue_manager.SessionLocal = TestingSessionLocal

# 3. Import App (after patching)
from fastapi.testclient import TestClient
from backend.src.main import app
from backend.src.api.routes import get_db
from backend.src.core.models import PrintJob
from backend.src.core.database import Base

# Override get_db dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# EXPLICITLY CREATE TABLES
print("Creating tables...")
Base.metadata.create_all(bind=engine)

def test_api_flow():
    # 4. Run Test with Context Manager
    with TestClient(app) as client:
        try:
            # Create Job
            print("Sending POST /api/jobs...")
            response = client.post("/api/jobs", json={
                "task_title": "API Test",
                "category": "Integration",
                "difficulty": 2
            })
            assert response.status_code == 200, response.text
            data = response.json()
            print(f"Created Job: {data}")
            job_id = data["id"]

            # Check History
            print("Sending GET /api/jobs...")
            response = client.get("/api/jobs")
            assert response.status_code == 200
            jobs = response.json()
            assert len(jobs) >= 1
            print(f"Found {len(jobs)} jobs.")

            # Wait for worker
            print("Waiting for worker...")
            time.sleep(3)

            # Check status again
            response = client.get(f"/api/jobs/{job_id}")
            data = response.json()
            print(f"Job Status after wait: {data['status']}")

            if data['status'] == 'COMPLETED':
                 print("Worker successfully processed the job!")
            else:
                 print("Worker might be slow or not running correctly.")

        finally:
            if os.path.exists(TEST_DB_FILE):
                os.remove(TEST_DB_FILE)
            if os.path.exists("printer_output"):
                shutil.rmtree("printer_output")

if __name__ == "__main__":
    test_api_flow()
