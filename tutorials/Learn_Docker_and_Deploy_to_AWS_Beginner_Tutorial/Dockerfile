FROM python:slim

WORKDIR /app

COPY . .

RUN python -m pip install -r requirements.txt

EXPOSE 8008

CMD ["python", "./app.py"]
