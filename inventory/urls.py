# -*- coding: utf-8 -*-
# -*- mode: python -*-
from django.contrib.auth.decorators import login_required
from django.urls import path

from inventory import views

app_name = "inventory"
urlpatterns = [
    path("", views.index, name="index"),
    path("orders/", views.OrderList.as_view(), name="orders"),
    path("orders/new/", login_required(views.order_entry), name="new_order"),
    path(r"orders/<int:pk>/", views.OrderView.as_view(), name="order"),
    path(
        "orders/<int:order_id>/place/",
        login_required(views.mark_order_placed),
        name="mark_order_placed",
    ),
    path("items/", views.ItemList.as_view(), name="items"),
    path("items/new/", login_required(views.item_entry), name="new_item"),
    path("items/<int:pk>/", views.ItemView.as_view(), name="item"),
    path(
        "items/<int:item_id>/order/",
        login_required(views.order_item_entry),
        name="add_item_to_order",
    ),
    path(
        "orderitems/<int:pk>/delete/",
        login_required(views.OrderItemDelete.as_view()),
        name="remove_item_from_order",
    ),
]
