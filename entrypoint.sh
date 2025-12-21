#!/bin/bash
set -e

echo "Waiting for PostgreSQL..."
while ! pg_isready -h db -p 5432 -U postgres; do
  sleep 1
done
echo "PostgreSQL is ready!"

echo "Running migrations..."
python -m django migrate --settings=inventory.tests.settings --noinput

echo "Creating superuser..."
python -m django shell --settings=inventory.tests.settings << 'PYEOF'
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="admin").exists():
    user = User.objects.create_superuser("admin", "admin@example.com", "admin123")
    print(f"Superuser created: {user.username}")
else:
    print("Superuser already exists")
PYEOF

echo "Creating regular user..."
python -m django shell --settings=inventory.tests.settings << 'PYEOF'
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="labuser").exists():
    user = User.objects.create_user("labuser", "labuser@lab.edu", "labuser123")
    user.is_staff = False
    user.is_superuser = False
    user.save()
    print(f"Regular user created: {user.username}")
else:
    print("Regular user already exists")
PYEOF

echo ""
echo "========================================"
echo "Django Lab Inventory is ready!"
echo "========================================"
echo "Access the application at: http://localhost:8003"
echo "Login credentials:"
echo "  Admin: admin / admin123"
echo "  User: labuser / labuser123"
echo "========================================"
echo ""

exec "$@"
