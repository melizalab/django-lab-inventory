docker run -it --rm \
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

## Quick Start (Docker)

The fastest way to run locally.

```bash
git clone https://github.com/beginnertodesign/django-lab-inventory.git
cd django-lab-inventory
docker-compose up --build
```

Then open http://localhost:8003 and log in:
- Admin: `admin` / `admin123`
- Regular user: `labuser` / `labuser123`

Helpful commands:

```bash
docker-compose down          # stop
docker-compose down -v       # stop and remove data
docker-compose logs -f       # follow logs
docker-compose restart web   # restart after code changes
```

## Manual Setup (Non-Docker)

1) Install dependencies

```bash
git clone https://github.com/beginnertodesign/django-lab-inventory.git
cd django-lab-inventory
pip install -e .

```

2) Apply migrations

```bash
python -m django migrate --settings=inventory.tests.settings
```

3) Create users

```bash
# Superuser (full access)
python -m django createsuperuser --settings=inventory.tests.settings

# Regular user (inventory only)
python -m django shell --settings=inventory.tests.settings <<'EOF'
from django.contrib.auth import get_user_model
User = get_user_model()
User.objects.get_or_create(username='labuser', defaults={
    'email': 'labuser@lab.edu', 'password': 'labuser123'
})[0].set_password('labuser123')
EOF
```

4) Run the server (default port 8003)

```bash
python -m django runserver 0.0.0.0:8003 --settings=inventory.tests.settings
```

## Access URLs

| Interface | Local URL | Notes |
|-----------|-----------|-------|
| User Login | http://127.0.0.1:8003/accounts/login/ | Normal users (labuser or any created user) |
| Inventory Dashboard | http://127.0.0.1:8003/university-laboratory-system/ | Redirects here after login |
| Admin Panel | http://127.0.0.1:8003/admin/ | Superusers only (e.g., admin) |

Codespaces/Dev Containers: use the PORTS tab and append the same paths (e.g., `/accounts/login/`).

## Users and Credentials

- Superuser: `admin` / `admin123` (access to inventory **and** admin panel)
- Regular user: `labuser` / `labuser123` (inventory only)
- To add more regular users:

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

## Features

- Inventory, vendors, manufacturers, categories, accounts
- Orders and order items with received tracking
- Search and filtering with django-filter
- Secure auth (Argon2 hashing, CSRF, session timeout, lockout)

## Testing

```bash
uv run pytest
# or
python -m pytest
```

Uses settings from `inventory/tests/settings.py`.

## Troubleshooting

- Port busy: `lsof -i :8003` then `kill <PID>` or choose another port with `runserver 0.0.0.0:8080`
- Reset admin password: `python -m django changepassword admin --settings=inventory.tests.settings`
- Apply migrations if models change: `python -m django migrate --settings=inventory.tests.settings`

## License

BSD 3-Clause. See [COPYING](COPYING).

## Support

Open an issue or PR at the repository: https://github.com/beginnertodesign/django-lab-inventory

<div align="center">

**Made with ❤️ for laboratory research**

</div>
Follow these steps if you prefer to set up the environment manually:
