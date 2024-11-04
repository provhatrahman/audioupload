FROM python:3.9-slim

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the application files
COPY . .

# Create music directory
RUN mkdir -p music

# Expose the port
EXPOSE 8080

# Command to run the application
CMD gunicorn --bind 0.0.0.0:8080 app:app 