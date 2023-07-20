# -*- coding: utf-8 -*-
# -*- mode: python -*-
from django import forms
from django.contrib.auth.models import User

from inventory.models import Account, Order


class NewOrderForm(forms.ModelForm):
    name = forms.CharField(label="Order Name")
    ordered_by = forms.ModelChoiceField(queryset=User.objects.filter(is_active=True))
    # make this only active accounts
    account = forms.ModelChoiceField(queryset=Account.objects.all(), required=False)

    class Meta:
        model = Order
        fields = ["name", "ordered_by", "account"]
