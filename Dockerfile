FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./app /app

COPY requirements.txt .

RUN pip install -r requirements.txt