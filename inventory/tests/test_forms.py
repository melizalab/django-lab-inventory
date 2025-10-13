# -*- coding: utf-8 -*-
# -*- mode: python -*-
import datetime

import pytest
from django.contrib.auth.models import User

from inventory.forms import ConfirmOrderForm
from inventory.models import Account, Order


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
