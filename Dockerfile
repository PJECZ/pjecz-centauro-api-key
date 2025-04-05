# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
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
ENV GUNICORN_WORKER_CLASS ${GUNICORN_WORKER_CLASS:-"uvicorn.workers.UvicornWorker"}

# Do not set the server for main.py
# Because the server is launched in the CMD command
ENV MAIN_APP_SERVER ""

# Run the web service on container startup
# Use gunicorn webserver with one worker process and 8 threads
# For environments with multiple CPU cores, increase the number of workers to be equal to the cores available
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling
CMD exec gunicorn \
    --bind 0.0.0.0:$PORT \
    --workers $GUNICORN_WORKERS \
    --worker-class $GUNICORN_WORKER_CLASS \
    --timeout 0 \
    pjecz_centauro_api_key.main:app

# Run the web service with CMD using brackets
# CMD ["gunicorn", "-b", "0.0.0.0:${PORT}", "-k", "uvicorn.workers.UvicornWorker", "-w", $GUNICORN_WORKERS, "-t", "0", "pjecz_centauro_api_key.main:app"]
