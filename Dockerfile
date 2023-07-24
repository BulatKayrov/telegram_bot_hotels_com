FROM python:3.10

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY callBack_data ./callBack_data
COPY commands ./commands
COPY database_sqlite ./database_sqlite
COPY handlers ./handlers
COPY keyboards ./keyboards
COPY storage_log ./storage_log
COPY templates_API ./templates_API
COPY create_bot.py .
COPY main.py .

CMD ["python", "main.py"]


