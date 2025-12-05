# Use the official lightweight Python image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Copy the Python application into the container
COPY app.py .

# Install PostgreSQL driver for Python
RUN pip install psycopg2-binary

# Default command to run when the container starts
CMD ["python", "app.py"]
