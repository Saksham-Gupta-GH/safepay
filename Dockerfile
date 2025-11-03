# Dockerfile for SafePay
# Builds a slim Python image and runs the Flask app with Gunicorn

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# system deps (if needed for cryptography, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# copy deps first to leverage Docker cache
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

# copy project
COPY . /app

# expose the port gunicorn binds to (see gunicorn.conf.py)
EXPOSE 10000

# Use gunicorn config file in repo
CMD ["gunicorn", "app:app", "-c", "gunicorn.conf.py"]
