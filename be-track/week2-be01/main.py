from fastapi import FastAPI, HTTPException

app = FastAPI()

# database for now
tasks = [
    {"id": 1, "title": "Buy groceries", "done": False},
    {"id": 2, "title": "Go to gym", "done": False},
    {"id": 3, "title": "Cook dinner", "done": True},
]
next_id = 4

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

@app.get("/health")
def health():
    return {"status": "ok"}