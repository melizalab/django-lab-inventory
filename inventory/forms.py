# -*- coding: utf-8 -*-
# -*- mode: python -*-
from django import forms
from django.contrib.auth.models import User

from inventory.models import Account, Order, Vendor, Item


class NewOrderForm(forms.ModelForm):
    name = forms.CharField(label="Order Name")
    ordered_by = forms.ModelChoiceField(queryset=User.objects.filter(is_active=True))
    # TODO make this only active accounts
    account = forms.ModelChoiceField(queryset=Account.objects.all(), required=False)

    class Meta:
        model = Order
        fields = ["name", "ordered_by", "account"]


class NewItemForm(forms.ModelForm):
    name = forms.CharField(label="Item Name")
    vendor = forms.ModelChoiceField(queryset=Vendor.objects.all(), required=True)
    catalog = forms.CharField(label="Vendor catalog number")
    manufacturer_number = forms.CharField(
        label="Manufacturer part number", required=False
    )
    order = forms.ModelChoiceField(
        queryset=Order.objects.filter(ordered=False),
        required=False,
        label="Add this item to an in-progress order",
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
