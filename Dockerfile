FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt

ENV PYTHONPATH="${PYTHONPATH}:/app/src"

CMD ["python", "src/main.py"]
