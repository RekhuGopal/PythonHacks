FROM python:3.10-alpine3.18

# WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

ENV PYTHONUNBUFFERED=1

CMD ["python" ,"app.py"]