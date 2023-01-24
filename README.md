
## lab-inventory

lab-inventory is a Django application used to track inventory and orders in the lab.

The admin interface is the primary tool used to create and update item records, but there is a growing collection of views that can be used to browse the database and generate orders in a format that can be sent off to our purchasing department.

lab-inventory is licensed for you to use under the BSD 3-Clause License. See COPYING for details

### Quick start

1. Requires Python 3.8+ and Django 4.0+

1. Install the package from pypi: `pip install django-labl-inventory`. Worth putting in a virtualenv.

1. Add `inventory` to your INSTALLED_APPS setting like this:

```python
INSTALLED_APPS = (
    ...
    'inventory',
)
```

2. Include the inventory URLconf in your project urls.py like this::

```python
re_path(r'^inventory/', include('inventory.urls')),
```

3. Run `python manage.py migrate` to create the inventory models.

4. Start the development server and visit http://127.0.0.1:8000/admin/inventory/
   to create items, vendors, manufacturers, etc. (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/inventory/ to use views.

### Bash example

Run [`sh example.sh`](example.sh) to create and run an example of django-lab-inventory. This is very outdated.
