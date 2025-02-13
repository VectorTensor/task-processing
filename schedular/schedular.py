import redis
import time
import json
import random
from sqlalchemy import create_engine, Column, BigInteger, JSON, Enum, TIMESTAMP, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Task(Base):
    __tablename__ = 'tasks'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    data = Column(JSON, nullable=False)
    status = Column(Enum('pending', 'processing', 'completed', 'failed', name='task_status'), default='pending')
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP'))

# Database connection
DATABASE_URL = "mysql+pymysql://user:password@localhost/mydatabase"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

# Query pending tasks
def get_pending_tasks():
    session = SessionLocal()
    try:
        pending_tasks = session.query(Task).filter(Task.status == 'pending').all()
        return pending_tasks
    finally:
        session.close()
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

def produce(task):
    message = data
    redis_client.lpush('task_queue', json.dumps(message))
    print(f"Produced: {message}")

if __name__ == "__main__":
    # produce()

    while True:
        tasks = get_pending_tasks()

        for task in tasks:
            produce(task.data)
        time.sleep(5)
