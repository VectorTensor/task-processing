
import redis
from sqlalchemy import create_engine, Column, BigInteger, JSON, Enum, TIMESTAMP, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
import logging


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    data = Column(JSON, nullable=False)
    status = Column(Enum('pending', 'processing', 'completed',
                    'failed', name='task_status'), default='pending')
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP, server_default=text(
        'CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP'))


# Database connection
DATABASE_URL = "mysql+pymysql://user:password@localhost/mydatabase"
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
# Query pending tasks


def get_pending_tasks():
    session = SessionLocal()
    try:
        pending_tasks = session.query(Task).filter(
            Task.status == 'pending').all()
        return pending_tasks
    finally:
        session.close()


def update_task_status(task_id, new_status):
    session = SessionLocal()
    try:
        task = session.query(Task).filter(Task.id == task_id).first()
        if task:
            task.status = new_status
            session.commit()
            print(f"Updated Task ID {task_id} to status '{new_status}'")
        else:
            print(f"Task ID {task_id} not found")
    finally:
        session.close()
