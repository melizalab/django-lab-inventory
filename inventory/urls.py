# -*- coding: utf-8 -*-
# -*- mode: python -*-
from django.contrib.auth.decorators import login_required
from django.urls import re_path

from inventory import views

app_name = "inventory"
urlpatterns = [
    re_path(r"^$", views.index, name="index"),
    re_path(r"^orders/$", views.OrderList.as_view(), name="orders"),
    re_path(
        r"^orders/new/$", login_required(views.OrderEntry.as_view()), name="new_order"
    ),
    re_path(r"^orders/(?P<pk>\d+)/$", views.OrderView.as_view(), name="order"),
    re_path(
        r"^orders/(?P<pk>\d+)/place/$",
        login_required(views.OrderMarkPlaced.as_view()),
        name="mark_order_placed",
    ),
    re_path(r"^items/$", views.ItemList.as_view(), name="items"),
    re_path(
        r"^items/new/$", login_required(views.ItemEntry.as_view()), name="new_item"
    ),
    re_path(r"^items/(?P<pk>\d+)/$", views.ItemView.as_view(), name="item"),
    re_path(
        r"^items/(?P<pk>\d+)/order/$",
        login_required(views.OrderItemEntry.as_view()),
        name="add_item_to_order",
    ),
    re_path(
        r"^orderitems/(?P<pk>\d+)/delete/$",
        login_required(views.OrderItemDelete.as_view()),
        name="remove_item_from_order",
    ),
]
