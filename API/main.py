# frontend --> api --> logic --> db --> response
# api/main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys, os

# Import taskmanager from src/logic.py - Updated for deployment
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
try:
    from src.logic import ProjectManager, TaskManager, UserManager
except ImportError:
    # Fallback for deployment environments
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from src.logic import ProjectManager, TaskManager, UserManager

app = FastAPI(title="Project Management API", version="1.0")

#allow frontend to access api
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # follow all origins (frontend apps)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#creating a task manager instance
task_manager = TaskManager()
project_manager = ProjectManager()
user_manager = UserManager()

#data models
class TaskCreate(BaseModel):
    '''
    schema for creating a task'''
    project_id: str
    title: str
    description: str
    assigned_to: str
    due_date: str
    status: str

class TaskUpdate(BaseModel):
    completed: bool

class ProjectCreate(BaseModel):
    '''
    schema for creating a project'''
    name: str
    description: str
    owner_id: str
    start_date: str
    end_date: str
    status: str

class UserCreate(BaseModel):
    '''
    schema for creating a user'''
    name: str
    email: str
    password_hash: str
    role: str

@app.get("/")
def home():
    '''
    check if the api is running
    '''
    return {
        "message": "Welcome to the Project Management API", 
        "status": "running",
        "docs": "/docs"
    }
@app.get("/tasks")
def get_tasks():
    '''
    get all tasks
    '''
    return task_manager.get_tasks()
@app.post("/tasks")
def create_task(task: TaskCreate):
    '''
    create a new task
    '''
    result = task_manager.add_task(task.project_id, task.title, task.description, task.assigned_to, task.due_date, task.status)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result
@app.put("/tasks/{task_id}")
def update_task(task_id: str, task: dict):
    '''
    update a task with new data
    '''
    result = task_manager.update_task(task_id, task)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@app.put("/tasks/{task_id}/status")
def update_task_status(task_id: str, task: TaskUpdate):
    '''
    mark it as complete or pending
    '''
    result = (
        task_manager.mark_complete(task_id)
        if task.completed else task_manager.mark_pending(task_id)
    )
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result
@app.delete("/tasks/{task_id}")
def delete_task(task_id: str):
    '''
    delete a task
    '''
    result = task_manager.remove_task(task_id)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

# More endpoints for projects and users can be added similarly
@app.get("/projects")
def get_projects():
    '''
    get all projects
    '''
    return project_manager.get_projects()
@app.post("/projects")
def create_project(project: ProjectCreate):
    '''
    create a new project
    '''
    result = project_manager.add_project(project.name, project.description, project.owner_id, project.start_date, project.end_date, project.status)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result
@app.put("/projects/{project_id}")
def update_project(project_id: str, project: dict):
    '''
    update a project
    '''
    result = project_manager.update_project(project_id, project)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result
@app.delete("/projects/{project_id}")
def delete_project(project_id: str):
    '''
    delete a project
    '''
    result = project_manager.remove_project(project_id)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result
@app.get("/users")
def get_users():
    '''
    get all users
    '''
    return user_manager.get_users()
@app.post("/users")
def create_user(user: UserCreate):
    '''
    create a new user
    '''
    result = user_manager.add_user(user.name, user.email, user.password_hash, user.role)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result
@app.put("/users/{user_id}")
def update_user(user_id: str, user: dict):
    '''
    update a user
    '''
    result = user_manager.update_user(user_id, user)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result
@app.delete("/users/{user_id}")
def delete_user(user_id: str):
    '''
    delete a user
    '''
    result = user_manager.remove_user(user_id)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)