# -*- coding: utf-8 -*-
# -*- mode: python -*-
import datetime
import types

import pytest
from django.contrib.auth.models import User

from inventory import forms as inventory_forms
from inventory import models as inventory_models
from inventory.forms import (
    ConfirmOrderForm,
    NewOrderForm,
    NewOrderItemForm,
)
from inventory.models import Account, Order


@pytest.fixture
def days_later(monkeypatch):
    """Simulate a long-running server process. This is to check that form dates are not getting frozen on import. """

    def advance(n_days):
        later = datetime.date.today() + datetime.timedelta(days=n_days)

        class FakeDate(datetime.date):
            @classmethod
            def today(cls):
                return later

        fake_datetime = types.SimpleNamespace(
            date=FakeDate, timedelta=datetime.timedelta
        )
        monkeypatch.setattr(inventory_forms, "datetime", fake_datetime)
        monkeypatch.setattr(inventory_models, "datetime", fake_datetime)
        return later

    return advance


@pytest.fixture
def user(db):
    """Create a test user"""
    return User.objects.create_user(username="testuser", password="testpass")


@pytest.fixture
def account(db):
    """Create a test account"""
    return Account.objects.create(
        code="TEST001",
        description="Test Account",
        expires_on=datetime.date.today() + datetime.timedelta(days=365),
    )


@pytest.fixture
def expired_account(db):
    """Create an expired account"""
    return Account.objects.create(
        code="EXP001",
        description="Expired Account",
        expires_on=datetime.date.today() - datetime.timedelta(days=1),
    )


@pytest.fixture
def order(db, user):
    """Create a test order"""
    return Order.objects.create(name="Test Order", requested_by=user)


@pytest.mark.django_db
def test_confirm_order_form_invalid_without_accounts(order, user):
    """Test that the form is invalid if no accounts are selected"""
    form_data = {
        "accounts": [],
        "requested_by": user.id,
    }
    form = ConfirmOrderForm(data=form_data, instance=order)
    assert not form.is_valid()
    assert "accounts" in form.errors
    assert "At least one account must be selected." in form.errors["accounts"]


@pytest.mark.django_db
def test_confirm_order_form_valid_with_one_account(order, user, account):
    """Test that the form is valid with one account selected"""
    form_data = {
        "accounts": [account.id],
        "requested_by": user.id,
    }
    form = ConfirmOrderForm(data=form_data, instance=order)
    assert form.is_valid()


@pytest.mark.django_db
def test_confirm_order_form_valid_with_multiple_accounts(order, user, account, db):
    """Test that the form is valid with multiple accounts selected"""
    account2 = Account.objects.create(
        code="TEST002",
        description="Test Account 2",
        expires_on=datetime.date.today() + datetime.timedelta(days=365),
    )
    form_data = {
        "accounts": [account.id, account2.id],
        "requested_by": user.id,
    }
    form = ConfirmOrderForm(data=form_data, instance=order)
    assert form.is_valid()


@pytest.mark.django_db
def test_confirm_order_form_excludes_expired_accounts(
    order, user, account, expired_account
):
    """Test that expired accounts are not in the queryset"""
    form = ConfirmOrderForm(instance=order)
    account_ids = [acc.id for acc in form.fields["accounts"].queryset]
    assert account.id in account_ids
    assert expired_account.id not in account_ids


@pytest.mark.django_db
def test_confirm_order_form_saves_accounts_correctly(order, user, account):
    """Test that saving the form creates OrderAccount relationships"""
    form_data = {
        "accounts": [account.id],
        "requested_by": user.id,
    }
    form = ConfirmOrderForm(data=form_data, instance=order)
    assert form.is_valid()
    saved_order = form.save()
    assert saved_order.accounts.count() == 1
    assert account in saved_order.accounts.all()


@pytest.mark.django_db
def test_confirm_order_form_initializes_with_existing_accounts(order, user, account):
    """Test that the form initializes with the order's existing accounts"""
    order.accounts.add(account)
    form = ConfirmOrderForm(instance=order)
    assert list(form.fields["accounts"].initial) == list(order.accounts.all())


@pytest.mark.django_db
def test_new_order_item_form_order_choices_use_current_date(user, days_later):
    """Orders placed after the process started must not be offered as in-progress"""
    order = Order.objects.create(name="Placed Later", requested_by=user)
    in_progress = Order.objects.create(name="In Progress", requested_by=user)
    later = days_later(10)
    order.mark_placed()
    assert order.placed_on == later

    form = NewOrderItemForm()
    order_ids = [o.id for o in form.fields["order"].queryset]
    assert in_progress.id in order_ids
    assert order.id not in order_ids


@pytest.mark.django_db
@pytest.mark.parametrize("form_class", [NewOrderForm, ConfirmOrderForm])
def test_account_choices_use_current_date(form_class, user, days_later):
    """Accounts that expired after the process started must not be offered"""
    soon_expired = Account.objects.create(
        code="SOON",
        description="Expires soon",
        expires_on=datetime.date.today() + datetime.timedelta(days=5),
    )
    still_valid = Account.objects.create(
        code="LATER",
        description="Expires much later",
        expires_on=datetime.date.today() + datetime.timedelta(days=365),
    )
    days_later(10)

    form = form_class()
    account_ids = [acc.id for acc in form.fields["accounts"].queryset]
    assert still_valid.id in account_ids
    assert soon_expired.id not in account_ids
