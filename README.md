## Task Processing System

## Overview
The Task Processing System is a distributed system designed to handle task scheduling, queuing, and execution efficiently. It consists of multiple services that work together to process tasks reliably.

## Components

### 1. **Consumer**
   - Retrieves tasks from the Redis queue and processes them accordingly.
   - Introduces random exceptions to simulate task failures.
   - If a task fails, it gets reinserted into the queue for retry.
   - If a task fails multiple times, it is moved to the Dead Letter Queue (DLQ).

### 2. **Scheduler**
   - Polls the MySQL database for pending tasks and pushes them to the Redis queue for processing.

### 3. **DLQ Processor**
   - Handles tasks that have failed multiple times by moving them to a Dead Letter Queue (DLQ) for further investigation.
   - Updates the tasks as failed in the database.

### 4. **MySQL Database**
   - Stores task data, including pending, in-progress, and completed tasks.

### 5. **Redis Message Queue**
   - Acts as a messaging system to queue tasks for processing asynchronously.

### 6. **Task Insert App**
   - Provides an interface or API to insert new tasks into the system for processing.

## Workflow
1. Tasks are inserted into the **MySQL database** via the **Task Insert App**.
2. The **Scheduler** polls the database and pushes pending tasks to the **Redis queue**.
3. The **Consumer** retrieves tasks from the queue and executes them.
   - If a task fails, it gets reinserted into the queue for retry.
   - If a task fails multiple times, it is moved to the **DLQ Processor** for further handling.
4. The **DLQ Processor** updates the tasks as failed in the **MySQL database**.
5. Successfully processed tasks are marked as completed in the **MySQL database**.

## Requirements
- Python 
- Docker 

## Installation & Running 
1. Clone the repository:
   ```sh
   git clone <repo_url>
   cd task-processing
   ```
2. Go to task-processing-services build docker compose
     ```sh
    cd task-processing-services
    docker compose up --build
    ```
3. Run the executors/consumers.(Check below for more information)

4. Insert New task using curl or postman 
    ```sh
    curl --location 'http://0.0.0.0:8000/tasks/' \
    --header 'Content-Type: application/json' \
    --data '{
        "message":"spiderman 3",
        "time":3
    }'
    ```


## Running the executors
Before running the executors install dependencies and run as many executors as you want
1. Create virtual environment.
    ```sh
   python -m venv venv
   ```
2. Run environment, install requirements and run as many executors.
   ```sh
   source venv/bin/activate
   pip install -r requirements.txt
   python consumer/executors.py
    ```

