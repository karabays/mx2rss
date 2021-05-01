FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./app /app

VOLUME [ "/data" ]

COPY requirements.txt .

RUN pip install -r requirements.txt