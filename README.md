
## lab-inventory

lab-inventory is a Django application used by our lab to to track inventory and orders. The basic idea is that users add items that can be purchased to the database, and then associate them with orders when they want to get the item. This allows us to quickly locate information about things we have purchased throughout the history of the lab. There is also some rudimentary support for keeping track of where items are located in the lab, when their warranties expire, and other useful information.

You'll probably need some familiarity with [Django](https://docs.djangoproject.com) and some knowledge about how to deploy a web application to use it.

lab-inventory is licensed for you to use under the BSD 3-Clause License. See COPYING for details

### Quick start

1. Requires Python 3.8+ and Django 4.0+

1. Install the package from pypi: `pip install django-lab-inventory`. Worth putting in a virtualenv.

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

