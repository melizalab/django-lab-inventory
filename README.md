# Django Lab Inventory

<div align="center">

[![Project Status](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)
[![Build Status](https://github.com/beginnertodesign/django-lab-inventory/actions/workflows/tests.yml/badge.svg)](https://github.com/beginnertodesign/django-lab-inventory/actions/workflows/tests.yml)
[![License](https://img.shields.io/pypi/l/django-lab-inventory.svg)](https://opensource.org/license/bsd-3-clause/)
[![Python Versions](https://img.shields.io/pypi/pyversions/django-lab-inventory.svg)](https://pypi.python.org/pypi/django-lab-inventory/)

**A Django app for laboratory inventory and order tracking**

</div>

---

## Overview

- Track items, locations, warranties, vendors, and orders in one place
- Attach items to purchase orders and track received items
- Secure authentication with separate user and admin logins
- Uses PostgreSQL and Django 6.0 (tested in dev container/Codespaces)

---

## Method 1: Docker Compose (Recommended - Easiest)

### Prerequisites
- Docker and Docker Compose installed

### Steps

**Option A: With Git Clone**
```bash
git clone https://github.com/beginnertodesign/django-lab-inventory.git
cd django-lab-inventory
docker-compose up --build
```

**Option B: Without Git Clone**
```bash
curl -L https://github.com/beginnertodesign/django-lab-inventory/archive/refs/heads/master.zip -o django-lab-inventory.zip
unzip django-lab-inventory.zip
cd django-lab-inventory-master
docker-compose up --build
```

**What happens during startup:**
- PostgreSQL database is initialized
- Django migrations are applied automatically
- Superuser (`admin`) and regular user (`labuser`) are created automatically
- Development server starts on port 8003

**Access the application:**
- Open: http://localhost:8003/accounts/login/
- Login credentials:
  - **Admin**: `admin` / `admin123`
  - **Regular user**: `labuser` / `labuser123`

### Useful Docker Commands
```bash
docker-compose down              # Stop containers
docker-compose down -v           # Stop and remove data
docker-compose logs -f           # View logs
docker-compose restart web       # Restart after code changes
```

---

## Method 2: GitHub Codespaces (No Local Installation)

### Steps

1. **Open Codespaces**
   - Visit: https://github.com/beginnertodesign/django-lab-inventory
   - Click: **Code** → **Codespaces** → **Create codespace on master**

2. **Wait for setup** (automatic dev container build)

3. **Start the application** (in Codespace terminal)
```bash
docker-compose up --build
```

4. **Access the application**
   - Go to **PORTS** tab in Codespaces
   - Click on port 8003 to open in browser
   - Navigate to `/accounts/login/`

---

## Method 3: Manual Setup (Without Docker)

### Prerequisites
- Python 3.11 or higher
- PostgreSQL 15 or higher
- pip

### Steps

1. **Download the repository**

**Option A: With Git Clone**
```bash
git clone https://github.com/beginnertodesign/django-lab-inventory.git
cd django-lab-inventory
```

**Option B: Without Git Clone**
```bash
curl -L https://github.com/beginnertodesign/django-lab-inventory/archive/refs/heads/master.zip -o django-lab-inventory.zip
unzip django-lab-inventory.zip
cd django-lab-inventory-master
```

2. **Install PostgreSQL and create database**
```bash
# On Ubuntu/Debian
sudo apt update
sudo apt install postgresql postgresql-contrib

# Start PostgreSQL
sudo systemctl start postgresql

# Create database
sudo -u postgres psql -c "CREATE DATABASE test_db;"
sudo -u postgres psql -c "CREATE USER postgres WITH PASSWORD 'postgres';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE test_db TO postgres;"
```

3. **Set environment variables**
```bash
export POSTGRES_DB=test_db
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=postgres
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
```

4. **Install Python dependencies**
```bash
pip install hatchling
pip install -e .
pip install argon2-cffi psycopg2-binary
```

5. **Run migrations**
```bash
python -m django migrate --settings=inventory.tests.settings
```

6. **Create superuser**
```bash
python -m django createsuperuser --settings=inventory.tests.settings
# Enter: username=admin, email=admin@example.com, password=admin123
```

7. **Create regular user**
```bash
python -m django shell --settings=inventory.tests.settings <<'EOF'
from django.contrib.auth import get_user_model
User = get_user_model()
user, created = User.objects.get_or_create(username='labuser', defaults={'email': 'labuser@lab.edu'})
user.set_password('labuser123')
user.is_staff = False
user.is_superuser = False
user.save()
print('User created:', user.username)
EOF
```

8. **Run the server**
```bash
python -m django runserver 0.0.0.0:8003 --settings=inventory.tests.settings
```

9. **Access the application**
   - Open: http://127.0.0.1:8003/accounts/login/

---

## Method 4: Direct Docker Run (Single Container)

```bash
# Download repository (without cloning)
curl -L https://github.com/beginnertodesign/django-lab-inventory/archive/refs/heads/master.zip -o django-lab-inventory.zip
unzip django-lab-inventory.zip
cd django-lab-inventory-master

# Build image
docker build -t django-lab-inventory .

# Run with SQLite (simpler, for testing)
docker run -it --rm -p 8003:8003 \
  -e POSTGRES_HOST= \
  django-lab-inventory \
  python -m django runserver 0.0.0.0:8003 --settings=inventory.tests.settings
```

---

## Access Points

| Interface | URL | Credentials |
|-----------|-----|-------------|
| Login Page | http://127.0.0.1:8003/accounts/login/ | admin/admin123 or labuser/labuser123 |
| Inventory Dashboard | http://127.0.0.1:8003/university-laboratory-system/ | Auto-redirects after login |
| Admin Panel | http://127.0.0.1:8003/admin/ | admin/admin123 (superuser only) |

**Note:** In Codespaces/Dev Containers, use the PORTS tab and append the paths (e.g., `/accounts/login/`).

---

## Users and Credentials

- **Superuser**: `admin` / `admin123` (access to inventory **and** admin panel)
- **Regular user**: `labuser` / `labuser123` (inventory only)

### Add More Users

```bash
python -m django shell --settings=inventory.tests.settings <<'EOF'
from django.contrib.auth import get_user_model
User = get_user_model()
user, created = User.objects.get_or_create(
    username='newuser', defaults={'email': 'new@lab.edu'}
)
user.set_password('strong_password')
user.is_staff = False
user.is_superuser = False
user.save()
print('Created' if created else 'Updated', user.username)
EOF
```

---

## Features

### Core Functionality
- Inventory, vendors, manufacturers, categories, accounts
- Orders and order items with received tracking
- Search and filtering with django-filter
- Secure auth (Argon2 hashing, CSRF, session timeout, lockout)

### What's New

#### Feature #1: QR Code Quick Checkout

We added a QR code system for equipment checkout. Lab members can now scan a QR code on any stock item to check it out - no need to navigate through menus or fill out forms. 

Each item gets its own unique QR code (using UUID tokens). When someone scans it with their phone, they just need to log in and set how many days they need the item. The system handles the rest - creates the checkout record, tracks who took what, and when it's due back.

The whole process takes about 10 seconds instead of the usual manual entry workflow. Plus, you can scan codes from any device since it's just a regular web URL. Everything still goes through proper authentication, so there's no security compromise.

Items track their status from checkout to return, making it easy to see what's currently out and who has it.

---

## Testing

Run the complete test suite to verify functionality:

```bash
uv run pytest
# or
python -m pytest
```

Uses settings from `inventory/tests/settings.py`.

### Testing the QR Checkout Feature

There are automated tests included for the QR checkout system:

```bash
# Run all tests
python -m pytest

# Just the QR checkout tests
python -m pytest inventory/tests/test_qr_quick_checkout.py -v

# With coverage
python -m pytest --cov=inventory --cov-report=html
```

**To test it manually:**

First, create a test item:
```bash
python -m django shell --settings=inventory.tests.settings <<'EOF'
from inventory.models import StockItem
item = StockItem.objects.create(
    name='Test Multimeter',
    sku='TM-001',
    description='Digital multimeter for testing'
)
print(f'QR URL: http://localhost:8003{item.get_qr_url()}')
print(f'QR Token: {item.qr_token}')
EOF
```

Then visit the URL that gets printed (or go to `http://localhost:8003/university-laboratory-system/quick-checkout/<token>/` with your token).

Log in as any user (like `labuser`/`labuser123`), pick how many days you need the item, and hit checkout. You should see a confirmation page with the item details and due date.

To check if it worked:
```bash
python -m django shell --settings=inventory.tests.settings <<'EOF'
from inventory.models import CheckoutRecord
records = CheckoutRecord.objects.all()
for r in records:
    print(f'{r.item.name} - {r.student.username} - Status: {r.status}')
    print(f'  Due: {r.due_date}')
EOF
```

The tests cover login requirements, token validation, record creation, due date math, and user tracking.

---

## Troubleshooting

### Docker build fails with "Readme file does not exist: README.rst"
This issue has been fixed in the latest version. If you encounter it:
```bash
# The pyproject.toml now correctly references README.md
# Pull the latest changes or ensure pyproject.toml has:
# readme = "README.md"
```

### Docker build fails with missing hatchling
The Dockerfile now automatically installs hatchling. If you face issues:
```bash
# Ensure your Dockerfile includes:
# pip install hatchling
```

### Entrypoint permission denied
If you see "exec: /app/entrypoint.sh: permission denied":
```bash
# Make entrypoint.sh executable before building
chmod +x entrypoint.sh
docker-compose up --build
```

### Port 8003 already in use
```bash
# Find process using port
lsof -i :8003

# Kill the process
kill <PID>

# Or use different port
python -m django runserver 0.0.0.0:8080 --settings=inventory.tests.settings
```

### Reset admin password
```bash
python -m django changepassword admin --settings=inventory.tests.settings
```

### Database issues
```bash
# Reset database (Docker)
docker-compose down -v
docker-compose up --build

# Reset database (Manual)
python -m django migrate --settings=inventory.tests.settings --run-syncdb
```

### View logs (Docker)
```bash
docker-compose logs -f web
```

### Apply migrations after model changes
```bash
python -m django migrate --settings=inventory.tests.settings
```

### Docker Compose version warning
If you see "the attribute `version` is obsolete" warning, it's safe to ignore. The `version` field in docker-compose.yml is deprecated but not required to be removed for functionality.

---

## License

BSD 3-Clause. See [COPYING](COPYING).

---

## Support

Open an issue or PR at the repository: https://github.com/beginnertodesign/django-lab-inventory

---

<div align="center">

**Made with ❤️ for laboratory research**

</div>
