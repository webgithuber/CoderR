FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY . .
EXPOSE 5000
CMD ["uvicorn" , "--host" ,"0.0.0.0", "--port" ,"5000","chat.asgi:application", "--workers","4"]
#"gunicorn", "--bind", "0.0.0.0:5000", "chat.asgi", "-w", "4", "-k", "uvicorn.workers.UvicornWorker"
#"python", "manage.py","runserver","0.0.0.0:5000"