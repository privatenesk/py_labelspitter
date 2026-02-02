from fastapi import FastAPI
from contextlib import asynccontextmanager
from backend.src.api import routes
from backend.src.core.database import Base, engine
from backend.src.worker.queue_manager import job_queue
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting up...")
    Base.metadata.create_all(bind=engine)
    job_queue.start()
    yield
    # Shutdown
    print("Shutting down...")
    job_queue.stop()

app = FastAPI(title="Haptic Jar API", lifespan=lifespan)

# CORS (Allow Frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, set to frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Haptic Productivity Jar API is running."}
