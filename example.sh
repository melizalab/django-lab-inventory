# Create virtual environment
python3 -m venv .venv

# source virtual environment
source .venv/bin/activate

# optionally customize inventory/templates/base_view.html

# install inventory
pip install -e .

# install django
pip install django==2.1.5

# create a django project
django-admin startproject invexample

# enter project folder
cd invexample

# add the "inventory" app to the project's settings.py
sed -ie "/INSTALLED_APPS = \[/a \ \ \ \ 'inventory'," invexample/settings.py

# edit the project's urls.py to create a path for inventory
#   add the django.urls include and re_path functions
sed -ie "s/^from django.urls import/from django.urls import include, re_path,/" invexample/urls.py
#   add redirection to inventory app
sed -ie "/urlpatterns = \[/a \ \ \ \ re_path(r'^inventory/', include('inventory.urls'))," invexample/urls.py

# migrate database
python manage.py migrate

# add an admin user
python manage.py createsuperuser

# run server
python manage.py runserver
# visit app at 127.0.0.1:8000/inventory
