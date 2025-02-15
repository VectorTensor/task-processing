from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel


from models.db_models import update_task_status, get_pending_tasks, Task, SessionLocal
app = FastAPI()


class TaskQuery(BaseModel):
    message: str
    time: int

    class Config:
        orm_mode = True


    


# Create a task endpoint


@app.post("/tasks/")
async def create_task(task: TaskQuery ):
    message = {
        "message": task.message,
        "time": task.time
    }
    db = SessionLocal()

    db_task = Task(data=message, status="pending")
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return {"id": db_task.id, "message": "Task created successfully"}
