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

### 🎯 NEW: QR-Assisted Quick Checkout

Streamline your laboratory equipment checkout process with QR code technology. Students and researchers can now checkout items instantly by scanning QR codes—no manual data entry required.

**Key Benefits:**
- ⚡ **Lightning-fast checkouts** - Scan and confirm in seconds
- 📱 **Mobile-friendly** - Works on any device with a camera
- 🔒 **Secure tracking** - Every checkout is logged with user, timestamp, and due date
- 🎨 **Intuitive interface** - Clean, professional design for optimal user experience

**How It Works:**
1. Each stock item receives a unique QR code with an embedded secure token
2. Users scan the QR code with their mobile device or camera
3. After authentication, they specify the checkout duration (default: 7 days)
4. The system creates a checkout record and provides instant confirmation
5. Items can be tracked through their complete checkout lifecycle (out → returned)

---

## Testing

Run the complete test suite to verify functionality:

```bash
uv run pytest
# or
python -m pytest
```

Uses settings from `inventory/tests/settings.py`.

### Testing the QR Quick Checkout Feature

The QR-assisted quick checkout feature includes comprehensive automated tests. To run them:

```bash
# Run all tests
python -m pytest

# Run only QR checkout tests
python -m pytest inventory/tests/test_qr_quick_checkout.py -v

# Run with coverage report
python -m pytest --cov=inventory --cov-report=html
```

**Manual Testing Steps:**

1. **Create a Stock Item with QR Code**
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

2. **Access the Quick Checkout Interface**
   - Navigate to the printed QR URL, or
   - Manually visit: `http://localhost:8003/university-laboratory-system/quick-checkout/<token>/`
   - Replace `<token>` with the UUID from step 1

3. **Test the Checkout Flow**
   - Log in with any user credentials (e.g., `labuser` / `labuser123`)
   - Specify the checkout duration (in days)
   - Click "Checkout Item"
   - Verify the success confirmation displays item details and due date

4. **Verify Checkout Records**
   ```bash
   python -m django shell --settings=inventory.tests.settings <<'EOF'
   from inventory.models import CheckoutRecord
   records = CheckoutRecord.objects.all()
   for r in records:
       print(f'{r.item.name} - {r.student.username} - Status: {r.status}')
       print(f'  Due: {r.due_date}')
   EOF
   ```

**Test Coverage Includes:**
- Authentication requirement for checkout
- QR token validation
- Checkout record creation with correct status
- Due date calculation
- User association with checkout records

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
