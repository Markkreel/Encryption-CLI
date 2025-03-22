# Use Python 3.11 as the base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and setup files
COPY requirements.txt setup.py ./

# Copy source code and tests
COPY src/ ./src/
COPY tests/ ./tests/

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install -e .

# Set environment variable for Python path
ENV PYTHONPATH=/app

# Command to run tests
CMD ["pytest", "tests/", "-v"]