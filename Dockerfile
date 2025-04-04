# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV GUNICORN_WORKERS ${GUNICORN_WORKERS:-2}

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies including gunicorn
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port the container will listen on (informational, Cloud Run uses $PORT)
EXPOSE 8080

# Gunicorn manages Uvicorn workers for ASGI compatibility
CMD exec gunicorn \
    --bind 0.0.0.0:$PORT \
    --workers $GUNICORN_WORKERS \
    --worker-class uvicorn.workers.UvicornWorker \
    --timeout 60 \
    pjecz_centauro_api_key.main:app
