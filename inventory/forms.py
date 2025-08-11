# -*- coding: utf-8 -*-
# -*- mode: python -*-
import datetime

from django import forms
from django.contrib.auth.models import User

from inventory.models import Account, Item, Order, OrderItem, Vendor


class NewOrderForm(forms.ModelForm):
    name = forms.CharField(label="Order Name")
    requested_by = forms.ModelChoiceField(
        queryset=User.objects.filter(is_active=True), label="Requested by"
    )
    account = forms.ModelChoiceField(
        queryset=Account.objects.exclude(expires__lt=datetime.date.today()),
        required=False,
    )

    class Meta:
        model = Order
        fields = ["name", "requested_by", "account"]


class ConfirmOrderForm(forms.ModelForm):
    account = forms.ModelChoiceField(
        queryset=Account.objects.exclude(expires__lt=datetime.date.today()),
        required=True,
    )
    requested_by = forms.ModelChoiceField(
        queryset=User.objects.filter(is_active=True),
        required=True,
        label="Requested by",
    )

    class Meta:
        model = Order
        fields = ["account", "requested_by"]


class OrderItemReceivedForm(forms.ModelForm):
    received_on = forms.DateField()

    class Meta:
        model = OrderItem
        fields = ["received_on"]
        

class NewItemForm(forms.ModelForm):
    name = forms.CharField(label="Item Name")
    vendor = forms.ModelChoiceField(queryset=Vendor.objects.all(), required=True)
    catalog = forms.CharField(label="Vendor catalog number")
    manufacturer_number = forms.CharField(
        label="Manufacturer part number", required=False
    )

    class Meta:
        model = Item
        fields = [
            "name",
            "category",
            "vendor",
            "catalog",
            "manufacturer",
            "manufacturer_number",
            "size",
            "unit",
            "parent_item",
            "comments",
        ]


class NewOrderItemForm(forms.ModelForm):
    order = forms.ModelChoiceField(
        queryset=Order.objects.not_placed(),
        required=True,
        label="Choose an in-progress order",
    )
    units_purchased = forms.IntegerField(label="Number of units to order")
    cost = forms.DecimalField(label="Current price per unit")

    class Meta:
        model = OrderItem
        fields = ["order", "units_purchased", "cost"]
