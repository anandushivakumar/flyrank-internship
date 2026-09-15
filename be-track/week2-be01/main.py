from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# database for now
tasks = [
    {"id": 1, "title": "Buy groceries", "done": False},
    {"id": 2, "title": "Go to gym", "done": False},
    {"id": 3, "title": "Cook dinner", "done": True},
]
next_id = 4

class TaskCreate(BaseModel):
    title: Optional[str] = None # so missing title doesn't crash before checking

@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/")
def root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(status_code=404, detail=f"Task {task_id} not found") # if no task matches

@app.post("/tasks", status_code=201)
def create_task(new_task: TaskCreate):
    global next_id
    if not new_task.title or not new_task.title.strip():
        raise HTTPException(status_code=400, detail="Title is required")

    task = {"id": next_id, "title": new_task.title, "done": False}
    tasks.append(task)
    next_id += 1
    return task

@app.get("/health")
def health():
    return {"status": "ok"}

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

@app.put("/tasks/{task_id}")
def update_task(task_id: int, updates: TaskUpdate):
    for task in tasks:
        if task["id"] == task_id:
            if updates.title is not None:
                if not updates.title.strip():
                    raise HTTPException(status_code=400, detail="Title cannot be empty")
                task["title"] = updates.title
            if updates.done is not None:
                task["done"] = updates.done
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return  
        
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")