lab-inventory
-------------

|ProjectStatus|_ |Version|_ |BuildStatus|_ |License|_ |PythonVersions|_

.. |ProjectStatus| image:: https://www.repostatus.org/badges/latest/active.svg
.. _ProjectStatus: https://www.repostatus.org/#active

.. |Version| image:: https://img.shields.io/pypi/v/django-lab-inventory.svg
.. _Version: https://pypi.python.org/pypi/django-lab-inventory/

.. |BuildStatus| image:: https://github.com/melizalab/django-lab-inventory/actions/workflows/tests.yml/badge.svg
.. _BuildStatus: https://github.com/melizalab/django-lab-inventory/actions/workflows/tests.yml

.. |License| image:: https://img.shields.io/pypi/l/django-lab-inventory.svg
.. _License: https://opensource.org/license/bsd-3-clause/

.. |PythonVersions| image:: https://img.shields.io/pypi/pyversions/django-lab-inventory.svg
.. _PythonVersions: https://pypi.python.org/pypi/django-lab-inventory/

lab-inventory is a Django application used by our lab to to track
inventory and orders. The basic idea is that users add items that can be
purchased to the database, and then associate them with orders when they
want to get the item. This allows us to quickly locate information about
things we have purchased throughout the history of the lab. There is
also some rudimentary support for keeping track of where items are
located in the lab, when their warranties expire, and other useful
information.

You’ll probably need some familiarity with
`Django <https://docs.djangoproject.com>`__ and some knowledge about how
to deploy a web application to use it.

lab-inventory is licensed for you to use under the BSD 3-Clause License.
See COPYING for details

Quick start
~~~~~~~~~~~

1. Requires Python 3.10+. Runs on Django 4.2 LTS and 5.1.

2. Install the package from pypi: ``pip install django-lab-inventory``.
   Worth putting in a virtualenv.

3. Add ``inventory`` to your INSTALLED_APPS setting like this:

.. code:: python

   INSTALLED_APPS = (
       ...
       'widget_tweaks',  # For form tweaking
       'django_filters',
       'inventory',
   )

2. Include inventory in ``urlpatterns`` in your project ``urls.py``. Some of
   the views link to the admin interface, so make sure that is included,
   too:

.. code:: python

       path("inventory/", include("inventory.urls")),
       path("admin/", admin.site.urls),

3. Run ``python manage.py migrate`` to create the inventory models.

4. Start the development server and visit
   http://127.0.0.1:8000/admin/inventory/ to create items, vendors,
   manufacturers, etc. (you’ll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/inventory/ to use views.

Development
~~~~~~~~~~~

Recommend using `uv <https://docs.astral.sh/uv/>`__ for development.

Run ``uv sync`` to create a virtual environment and install
dependencies. ``uv sync --no-dev --frozen`` for deployment.

Testing: ``uv run pytest``. Requires a test database, will use settings
from ``inventory/test/settings.py``.
