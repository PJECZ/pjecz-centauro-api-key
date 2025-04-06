# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables for Python
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file into the container
COPY requirements.txt ./

# Install dependencies including gunicorn
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . ./

# PORT is automatically provided by Cloud Run, typically 8080
# EXPOSE 8080

# Run the web service on container startup
# Set desired Gunicorn worker count (adjust based on Cloud Run CPU/Memory and expected load)
# Cloud Run v2 usually provides at least 1 CPU, v1 might share, start with 1 or 2
# Use Uvicorn as the worker class for async support
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling
CMD exec gunicorn \
    --bind 0.0.0.0:$PORT \
    --workers 1 \
    --threads 8 \
    --worker-class uvicorn.workers.UvicornWorker \
    --timeout 0 \
    pjecz_centauro_api_key.main:app
