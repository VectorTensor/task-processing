from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Database Configuration
DATABASE_URL = "mysql+mysqlconnector://your_username:your_password@localhost/your_database_name"

# SQLAlchemy setup
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Task model
class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(BigInteger, primary_key=True,autoincrement=True)
    # title = Column(String(255), nullable=False)
    # description = Column(String, nullable=True)
    data = Column(JSON, nullable=False)
    status = Column(Enum('pending','processing','completed','failed'), default='pending')
    created_at = 

# Create the tasks table
Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI()

# Pydantic Task schema
class Task(BaseModel):
    title: str
    description: str | None = None

    class Config:
        orm_mode = True

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a task endpoint
@app.post("/tasks/")
async def create_task(task: Task, db: Session = Depends(get_db)):
    db_task = TaskModel(title=task.title, description=task.description)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return {"id": db_task.id, "message": "Task created successfully"}
