# Placement-Portal-Application-V2
MAD 2 Project - MAY 2026 TERM

# Placement Portal -- How to Run

## 1. Prerequisites

Install:

-   Python
-   Node.js and npm
-   Redis

Check installations:

``` bash
python --version
node --version
npm --version
redis-server --version
```

## 2. Backend Setup

Open a terminal and go to the backend folder:

``` bash
cd backend
```

Create a virtual environment:

``` bash
python -m venv venv
```

Activate it.

### Windows

``` bash
venv\Scripts\activate
```

### Linux/macOS

``` bash
source venv/bin/activate
```

Install dependencies:

``` bash
pip install -r requirements.txt
```

## 3. Start Redis

Open a new terminal:

``` bash
redis-server
```

Keep Redis running.

## 4. Start Flask Backend

Open another terminal:

``` bash
cd backend
source venv/bin/activate
python app.py
```

Flask will run at:

``` text
http://localhost:5000
```

Keep Flask running.

## 5. Start Celery Worker

Open another terminal:

``` bash
cd backend
source venv/bin/activate
py -m celery -A celery_worker.celery_app worker --loglevel=info
```

Keep the Celery worker running.

> On Windows, if the normal worker has multiprocessing issues, use:

``` bash
py -m celery -A celery_worker.celery_app worker --loglevel=info --pool=solo
```

## 6. Start Celery Beat

Open another terminal:

``` bash
cd backend
source venv/bin/activate
py -m celery -A celery_worker.celery_app beat --loglevel=info
```

Keep Celery Beat running.

Celery Beat sends scheduled tasks to the Celery worker.

## 7. Start Vue Frontend

Open another terminal:

``` bash
cd frontend
npm install
npm run dev
```

The frontend will normally run at:

``` text
http://localhost:5173
```

## 8. Open the Application

Open:

``` text
http://localhost:5173
```

## 9. Terminals Required

Keep all five services running.

### Terminal 1 -- Redis

``` bash
redis-server
```

### Terminal 2 -- Flask

``` bash
cd backend
source venv/bin/activate
python app.py
```

### Terminal 3 -- Celery Worker

``` bash
cd backend
source venv/bin/activate
py -m celery -A celery_worker.celery_app worker --loglevel=info --pool=solo
```

### Terminal 4 -- Celery Beat

``` bash
cd backend
source venv/bin/activate
py -m celery -A celery_worker.celery_app beat --loglevel=info
```

### Terminal 5 -- Vue

``` bash
cd frontend
npm install
npm run dev
```

## 10. Services

  Service         Address / Purpose
  --------------- ---------------------------
  Vue             `http://localhost:5173`
  Flask           `http://localhost:5000`
  Redis           `localhost:6379`
  Celery Worker   Executes background tasks
  Celery Beat     Sends scheduled tasks



## 11. Stop the Application

Press:

``` bash
Ctrl + C
```

in each terminal to stop:

-   Vue
-   Flask
-   Celery Worker
-   Celery Beat
-   Redis

To exit the Python virtual environment:

``` bash
deactivate
```

