"""
Simple REST API with FastAPI
===========================

A lightweight REST API for task management built using FastAPI.
Implements CRUD (Create, Read, Update, Delete) operations.

Endpoints:
    GET    /api/tasks          - Retrieve all tasks
    GET    /api/tasks/<id>    - Retrieve a specific task
    POST   /api/tasks          - Create a new task
    PUT    /api/tasks/<id>    - Update an existing task
    DELETE /api/tasks/<id>    - Delete a task

Usage:
    Run the application: uvicorn app:app --reload
    API will be available at: http://localhost:8000

Requirements:
    - FastAPI
    - uvicorn

Installation:
    pip install fastapi uvicorn

Author: Senior Software Engineer
Version: 1.0.0
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI application
app = FastAPI(
    title="Task Management API",
    description="A simple REST API for task management built with FastAPI",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============== Data Models ==============

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, description="Task title (required)")
    description: Optional[str] = Field("", description="Task description")
    done: Optional[bool] = Field(False, description="Task completion status")

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    done: Optional[bool] = Field(None, description="Task completion status")

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    done: bool

class TaskListResponse(BaseModel):
    success: bool
    tasks: List[TaskResponse]
    total: int

class MessageResponse(BaseModel):
    success: bool
    message: str

class ErrorResponse(BaseModel):
    success: bool
    error: str

# ============== In-Memory Data Store ==============

tasks_db: List[dict] = [
    {"id": 1, "title": "Buy groceries", "description": "Milk, Bread, Eggs, Butter, Cheese", "done": False},
    {"id": 2, "title": "Learn FastAPI REST API", "description": "Build a complete REST API from scratch", "done": True},
    {"id": 3, "title": "Complete project documentation", "description": "Write comprehensive documentation for the API", "done": False}
]

next_task_id = 4


# ============== Error Handlers ==============

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "error": exc.detail}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"success": False, "error": "Internal server error"}
    )


# ============== API Routes ==============

@app.get("/")
async def root():
    """Root endpoint - serves the UI"""
    return FileResponse("index.html")


@app.get("/api/health", response_model=MessageResponse)
async def health_check():
    """
    Health check endpoint to verify API is running.

    Returns:
        JSON response indicating API health status
    """
    return MessageResponse(success=True, message="API is running properly")


@app.get("/api/tasks", response_model=TaskListResponse)
async def get_all_tasks():
    """
    Retrieve all tasks from the API.

    Returns:
        JSON response containing list of all tasks
    """
    logger.info(f"GET /api/tasks - Retrieved {len(tasks_db)} tasks")
    return TaskListResponse(
        success=True,
        tasks=[TaskResponse(**task) for task in tasks_db],
        total=len(tasks_db)
    )


@app.get("/api/tasks/{task_id}", response_model=dict)
async def get_task(task_id: int):
    """
    Retrieve a specific task by its ID.

    Args:
        task_id: The unique identifier of the task

    Returns:
        JSON response containing the task data
    """
    task = next((task for task in tasks_db if task["id"] == task_id), None)

    if task:
        logger.info(f"GET /api/tasks/{task_id} - Task found")
        return {"success": True, "task": TaskResponse(**task)}
    else:
        logger.warning(f"GET /api/tasks/{task_id} - Task not found")
        raise HTTPException(status_code=404, detail="Task not found")


@app.post("/api/tasks", response_model=dict, status_code=201)
async def create_task(task: TaskCreate):
    """
    Create a new task.

    Args:
        task: Task data from request body

    Returns:
        JSON response containing the created task
    """
    global next_task_id

    new_task = {
        "id": next_task_id,
        "title": task.title.strip(),
        "description": task.description.strip() if task.description else "",
        "done": task.done
    }

    tasks_db.append(new_task)
    next_task_id += 1

    logger.info(f"POST /api/tasks - Task created with ID: {new_task['id']}")
    return {
        "success": True,
        "message": "Task created successfully",
        "task": TaskResponse(**new_task)
    }


@app.put("/api/tasks/{task_id}", response_model=dict)
async def update_task(task_id: int, task_update: TaskUpdate):
    """
    Update an existing task.

    Args:
        task_id: The unique identifier of the task to update
        task_update: Updated task data

    Returns:
        JSON response containing the updated task
    """
    task = next((task for task in tasks_db if task["id"] == task_id), None)

    if not task:
        logger.warning(f"PUT /api/tasks/{task_id} - Task not found")
        raise HTTPException(status_code=404, detail="Task not found")

    # Update only provided fields
    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if field == "title" and value:
            value = value.strip()
        if field == "description" and value:
            value = value.strip()
        task[field] = value

    logger.info(f"PUT /api/tasks/{task_id} - Task updated successfully")
    return {
        "success": True,
        "message": "Task updated successfully",
        "task": TaskResponse(**task)
    }


@app.delete("/api/tasks/{task_id}", response_model=dict)
async def delete_task(task_id: int):
    """
    Delete a task by its ID.

    Args:
        task_id: The unique identifier of the task to delete

    Returns:
        JSON response indicating success or failure
    """
    global tasks_db

    task_index = next(
        (index for index, task in enumerate(tasks_db) if task["id"] == task_id),
        None
    )

    if task_index is not None:
        deleted_task = tasks_db.pop(task_index)
        logger.info(f"DELETE /api/tasks/{task_id} - Task deleted successfully")
        return {
            "success": True,
            "message": "Task deleted successfully",
            "deleted_task": TaskResponse(**deleted_task)
        }
    else:
        logger.warning(f"DELETE /api/tasks/{task_id} - Task not found")
        raise HTTPException(status_code=404, detail="Task not found")


# ============== Main ==============

if __name__ == "__main__":
    import uvicorn
    print("=" * 60)
    print("Starting Simple REST API with FastAPI")
    print("=" * 60)
    print("\nAPI Endpoints:")
    print("  GET    /api/tasks          - Get all tasks")
    print("  GET    /api/tasks/<id>     - Get task by ID")
    print("  POST   /api/tasks          - Create new task")
    print("  PUT    /api/tasks/<id>     - Update task")
    print("  DELETE /api/tasks/<id>     - Delete task")
    print("  GET    /api/health         - Health check")
    print("\nServer running at: http://localhost:8000")
    print("API Docs available at: http://localhost:8000/docs")
    print("Press CTRL+C to stop the server")
    print("=" * 60)
    uvicorn.run(app, host="0.0.0.0", port=8000)
