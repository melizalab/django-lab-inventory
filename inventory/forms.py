# -*- coding: utf-8 -*-
# -*- mode: python -*-
import datetime

from django import forms
from django.contrib.auth.models import User

from inventory.models import Account, Item, Order, OrderAccount, OrderItem, Vendor


class NewOrderForm(forms.ModelForm):
    name = forms.CharField(label="Order Name")
    requested_by = forms.ModelChoiceField(
        queryset=User.objects.filter(is_active=True), label="Requested by"
    )
    accounts = forms.ModelMultipleChoiceField(
        queryset=Account.objects.exclude(expires__lt=datetime.date.today()),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Accounts (select all that apply)",
    )

    def save(self, commit=True):
        order = super().save(commit=commit)
        if commit:
            # Clear existing accounts and add selected ones
            order.accounts.clear()
            for account in self.cleaned_data["accounts"]:
                OrderAccount.objects.create(order=order, account=account)
        return order

    class Meta:
        model = Order
        fields = ["name", "requested_by", "accounts"]


class ConfirmOrderForm(forms.ModelForm):
    accounts = forms.ModelMultipleChoiceField(
        queryset=Account.objects.exclude(expires__lt=datetime.date.today()),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Accounts (select at least one)",
    )
    requested_by = forms.ModelChoiceField(
        queryset=User.objects.filter(is_active=True),
        required=True,
        label="Requested by",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["accounts"].initial = self.instance.accounts.all()

    def clean_accounts(self):
        """Ensure at least one account is selected when confirming order"""
        accounts = self.cleaned_data.get("accounts")
        if not accounts:
            raise forms.ValidationError("At least one account must be selected.")
        return accounts

    def save(self, commit=True):
        order = super().save(commit=commit)
        if commit:
            order.accounts.clear()
            for account in self.cleaned_data["accounts"]:
                OrderAccount.objects.create(order=order, account=account)
        return order

    class Meta:
        model = Order
        fields = ["accounts", "requested_by"]


class OrderItemReceivedForm(forms.ModelForm):
    arrived_on = forms.DateField(widget=forms.widgets.DateInput(attrs={"type": "date"}))

    class Meta:
        model = OrderItem
        fields = ["arrived_on", "location", "serial", "uva_equip"]


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
