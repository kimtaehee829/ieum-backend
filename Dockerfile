FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8080

CMD exec gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8080} --workers 2 --threads 8 --timeout 0