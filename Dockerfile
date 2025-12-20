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

# Copy project files
COPY . /app/

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -e . && \
    pip install argon2-cffi psycopg2-binary

# Create entrypoint script
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
echo "Waiting for PostgreSQL..."\n\
while ! pg_isready -h db -p 5432 -U postgres; do\n\
  sleep 1\n\
done\n\
echo "PostgreSQL is ready!"\n\
\n\
echo "Running migrations..."\n\
python -m django migrate --settings=inventory.tests.settings --noinput\n\
\n\
echo "Creating superuser..."\n\
python -m django shell --settings=inventory.tests.settings << EOF\n\
from django.contrib.auth import get_user_model\n\
User = get_user_model()\n\
if not User.objects.filter(username="admin").exists():\n\
    user = User.objects.create_superuser("admin", "admin@example.com", "admin123")\n\
    print(f"Superuser created: {user.username}")\n\
else:\n\
    print("Superuser already exists")\n\
EOF\n\
\n\
echo ""\n\
echo "========================================"\n\
echo "Django Lab Inventory is ready!"\n\
echo "========================================"\n\
echo "Access the application at: http://localhost:8003"\n\
echo "Login credentials:"\n\
echo "  Username: admin"\n\
echo "  Password: admin123"\n\
echo "========================================"\n\
echo ""\n\
\n\
exec "$@"\n\
' > /app/entrypoint.sh && chmod +x /app/entrypoint.sh

EXPOSE 8003

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["python", "-m", "django", "runserver", "0.0.0.0:8003", "--settings=inventory.tests.settings"]
