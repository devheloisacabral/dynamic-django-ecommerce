FROM python:3.9-slim

# Postgre dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt


COPY . /app/

EXPOSE 8000

ENV PYTHONUNBUFFERED=1

CMD ["bash", "-c", "python manage.py migrate && python manage.py runserver 127.0.0.1:8000"]
CMD ["bash", "-c", "python manage.py migrate && python manage.py migrate"]
CMD ["bash", "-c", "python manage.py migrate && python manage.py collectstatic"]
