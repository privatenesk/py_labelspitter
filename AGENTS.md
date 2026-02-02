# Haptic Productivity Jar - Developer Guide

## Project Overview
This project is an IoT application for a Raspberry Pi Zero. It receives task completion data via a REST API, generates a physical label, and prints it. The label length corresponds to the task difficulty.

## Architecture
- **Backend**: Python (FastAPI).
- **Frontend**: Nuxt 3 (Vue.js).
- **Database**: PostgreSQL.
- **Queue**: In-memory producer/consumer pattern.
- **Hardware**: Target is Raspberry Pi Zero with a thermal printer (e.g., Brother QL-800).

## Directory Structure
- `backend/`: Python source code.
- `frontend/`: Nuxt source code.
- `docker-compose.yml`: Orchestration for dev/test.

## JSON Payload Schema
The input payload for creating a job (`POST /jobs`) should follow this structure:
```json
{
  "task_title": "Task Name",
  "category": "Work",
  "difficulty": 3,
  "config": {
    "fillers": "arrows",
    "scaling_factor": 1.0
  }
}
```

## Optimizations for Pi Zero
- Lightweight backend (FastAPI).
- Async processing for printing (blocking I/O).
- Minimal Docker images (Alpine/Slim).
