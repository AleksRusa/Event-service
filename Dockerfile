FROM python:3.12.5-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD ["sh", "-c", "alembic upgrade head && python src/main.py --host 0.0.0.0 --port 8000"]