FROM python:3.9-slim

WORKDIR /app

# Install development dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install flask-debug watchdog

# Don't copy the code - we'll mount it as a volume
VOLUME ["/app"]

EXPOSE 5000

# Use Flask development server
CMD ["python", "app.py"] 