# Use Python 3.13 slim image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml ./
COPY README.md ./
COPY redisq/ ./redisq/
COPY example_usage.py ./
COPY test_redisq.py ./

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Install additional dependencies for testing
RUN pip install --no-cache-dir requests pytest

# Expose port (if needed for web apps)
EXPOSE 8000

# Default command to run tests
CMD ["python", "test_redisq.py"]
