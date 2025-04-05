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

# Set desired Gunicorn worker count (adjust based on Cloud Run CPU/Memory and expected load)
# Cloud Run v2 usually provides at least 1 CPU, v1 might share
# Start with 1 or 2
ENV GUNICORN_WORKERS ${GUNICORN_WORKERS:-2}

# Set the Gunicorn worker class to use uvicorn ASGI workers
ENV GUNICORN_WORKER_CLASS ${GUNICORN_WORKER_CLASS:-"uvicorn.workers.UvicornWorker"}

# Do not set the server for main.py, because the server is launched in the CMD command
ENV MAIN_APP_SERVER ""

# Run the web service on container startup
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling
CMD exec gunicorn \
    --bind 0.0.0.0:$PORT \
    --workers $GUNICORN_WORKERS \
    --worker-class $GUNICORN_WORKER_CLASS \
    --timeout 0 \
    pjecz_centauro_api_key.main:app
