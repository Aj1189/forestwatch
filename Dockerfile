FROM python:3.10-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && apt-get update && apt-get install -y supervisor

COPY backend/ ./backend/
COPY frontend/ ./frontend/
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 5000 8000

CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
