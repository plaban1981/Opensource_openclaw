# OpenClaw - Agentic Framework

A multi-agent AI framework using CrewAI with Ollama (minimax-m2.5:cloud).

## Features

- **Researcher Agent** - Web search and research capabilities
- **Coder Agent** - Code writing and file management
- **Reviewer Agent** - Code review and quality checks
- **Executor Agent** - Code execution and task completion

## Setup

1. Install dependencies:
```bash
pip install -e ".[dev]"
```

2. Ensure Ollama is running with the minimax-m2.5:cloud model:
```bash
ollama serve
ollama pull minimax-m2.5:cloud
```

3. Run the framework:
```bash
python main.py
```

## Configuration

- Default model: `minimax-m2.5:cloud`
- Default base URL: `http://localhost:11434`
- Temperature: `0.7`

## Usage

```python
from main import create_crew, create_simple_crew

# Simple crew (Researcher + Coder)
crew = create_simple_crew("Your task here")
result = crew.kickoff()

# Full crew (all 4 agents)
crew = create_crew("Your task here")
result = crew.kickoff()
```

## Available Tools

- `ddg_search` - DuckDuckGo web search
- `fetch_web_content` - Fetch web page content
- `execute_code` - Execute Python/JavaScript/bash code
- `write_file` - Write content to files
- `read_file` - Read content from files


 # run directly
  python app.py

  API Endpoints

  - GET /api/tasks - Get all tasks
  - GET /api/tasks/{id} - Get task by ID
  - POST /api/tasks - Create new task
  - PUT /api/tasks/{id} - Update task
  - DELETE /api/tasks/{id} - Delete task
  - GET /api/health - Health check
  - GET /docs - Interactive API documentation (Swagger UI)

## Files 

  ┌────────────┬───────────────────────────┐
  │    File    │        Description        │
  ├────────────┼───────────────────────────┤
  │ app.py     │ FastAPI backend with CORS │
  ├────────────┼───────────────────────────┤
  │ index.html │ Beautiful light-themed UI │
  ├────────────┼───────────────────────────┤
  │ main.py    │ OpenClaw framework        │
  └────────────┴───────────────────────────┘

## To Run
```
  cd C:\Users\nayak\Documents\my_open_claw
  uvicorn app:app --reload

  Then open: http://localhost:8000
```
##  UI Features

  - Clean Light Theme with modern gradients
  - Stats Dashboard - Total, completed, pending tasks
  - Task Form - Add new tasks with title & description
  - Task List - View all tasks with filters (All/Pending/Completed)
  - CRUD Actions - Create, edit, delete, toggle completion
  - Toast Notifications - Success/error feedback
  - Modal Editor - Edit tasks in a popup
  - API Status Indicator - Shows if backend is online/offline
  - Responsive Design - Works on mobile & desktop
  - Smooth Animations - Modern transitions & hover effects


## Sample Usage Examples

  1. Start the API Server
  ```
  cd C:\Users\nayak\Documents\my_open_claw
  uvicorn app:app --reload
  ```
  2. Open the UI
  ```
  Navigate to: http://localhost:8000
  ```
  3. Using the UI

  Create a Task:
  1. Enter task title: "Learn FastAPI"
  2. Enter description: "Build REST APIs with FastAPI"
  3. Click "Add Task"

  Complete a Task:
  - Click the circular checkbox next to a task

  Edit a Task:
  - Click the edit icon (pencil)
  - Modify title/description
  - Click "Save Changes"

  Delete a Task:
  - Click the trash icon
  - Confirm deletion

  Filter Tasks:
  - Click "All", "Pending", or "Completed" buttons

  ---
  4. Using the API Directly

  # Get all tasks
  curl http://localhost:8000/api/tasks

  # Create a new task
  curl -X POST http://localhost:8000/api/tasks \
    -H "Content-Type: application/json" \
    -d '{"title": "Buy groceries", "description": "Milk, Bread, Eggs", "done": false}'

  # Update a task
  curl -X PUT http://localhost:8000/api/tasks/1 \
    -H "Content-Type: application/json" \
    -d '{"done": true}'

  # Delete a task
  curl -X DELETE http://localhost:8000/api/tasks/1

  # Health check
  curl http://localhost:8000/api/health

  5. API Documentation

  Open: http://localhost:8000/docs (Swagger UI)

  ---
  The UI will show:
  - 3 pre-loaded sample tasks
  - Real-time stats (Total/Completed/Pending)
  - Beautiful toast notifications for all actions
