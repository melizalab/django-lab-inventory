# Use Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy entrypoint first
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Copy project files
COPY . /app/

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install hatchling && \
    pip install -e . && \
    pip install -r requirements-dev.txt && \
    pip install argon2-cffi psycopg2-binary

EXPOSE 8003

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["python", "-m", "django", "runserver", "0.0.0.0:8003", "--settings=inventory.tests.settings"]

