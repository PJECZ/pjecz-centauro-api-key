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

# Expose the port the container will listen on (informational, Cloud Run uses $PORT)
EXPOSE 8080

# Run the web service on container startup
# Use gunicorn webserver with one worker process and 8 threads
# For environments with multiple CPU cores, increase the number of workers to be equal to the cores available
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 pjecz_centauro_api_key.main:app
