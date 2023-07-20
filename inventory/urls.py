from django.urls import re_path

from inventory import views

app_name = "inventory"
urlpatterns = [
    re_path(r"^$", views.index, name="index"),
    re_path(r"^orders/$", views.OrderList.as_view(), name="orders"),
    re_path(r"^orders/(?P<pk>\d+)/$", views.OrderView.as_view(), name="order"),
    re_path(r"^items/$", views.ItemList.as_view(), name="items"),
    re_path(r"^items/(?P<pk>\d+)/$", views.ItemView.as_view(), name="item"),
]
