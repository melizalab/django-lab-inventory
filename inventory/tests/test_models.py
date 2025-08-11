# -*- mode: python -*-

import pytest
from django.contrib.auth import get_user_model

from inventory.models import (
    Account,
    Category,
    Item,
    Order,
    OrderItem,
    Unit,
    Vendor,
)


@pytest.fixture
def sentinel_user():
    return get_user_model().objects.get_or_create(username="deleted")[0]


@pytest.mark.django_db
def test_orderitem_cost(sentinel_user):
    category = Category.objects.create(name="glues and pastes")
    unit = Unit.objects.create(name="each")
    vendor = Vendor.objects.create(name="Unicorn Dispensary")
    account = Account.objects.create(code="1234", description="unicorn paste fund")
    item = Item.objects.create(
        name="unicorn paste",
        category=category,
        unit=unit,
        vendor=vendor,
        catalog="UPASTE1",
    )
    order = Order.objects.create(
        name="yearly unicorn paste supply", requested_by=sentinel_user
    )
    order.add_account(account)

    orderitem = OrderItem.objects.create(
        item=item, order=order, units_purchased=10, cost=20
    )

    assert orderitem.total_cost() == 200
    assert order.total_cost() == 200


@pytest.mark.django_db
def test_order_cost(sentinel_user):
    category = Category.objects.create(name="glues and pastes")
    unit = Unit.objects.create(name="each")
    vendor = Vendor.objects.create(name="Unicorn Dispensary")
    account = Account.objects.create(code="1234", description="unicorn paste fund")
    order = Order.objects.create(
        name="yearly unicorn paste supply", requested_by=sentinel_user
    )
    order.add_account(account)

    item_1 = Item.objects.create(
        name="unicorn paste",
        category=category,
        unit=unit,
        vendor=vendor,
        catalog="UPASTE1",
    )
    item_2 = Item.objects.create(
        name="unicorn paste adapter",
        category=category,
        unit=unit,
        vendor=vendor,
        catalog="UPADAPT",
    )
    order.add_item(item=item_1, n_units=10, cost_per_unit=20)
    order.add_item(item=item_2, n_units=1, cost_per_unit=200)

    assert order.total_cost() == 400


@pytest.mark.django_db
def test_order_counts(sentinel_user):
    category = Category.objects.create(name="glues and pastes")
    unit = Unit.objects.create(name="each")
    vendor = Vendor.objects.create(name="Unicorn Dispensary")
    account = Account.objects.create(code="1234", description="unicorn paste fund")
    order = Order.objects.create(
        name="yearly unicorn paste supply", requested_by=sentinel_user
    )
    order.add_account(account)

    item_1 = Item.objects.create(
        name="unicorn paste",
        category=category,
        unit=unit,
        vendor=vendor,
        catalog="UPASTE1",
    )
    item_2 = Item.objects.create(
        name="unicorn paste adapter",
        category=category,
        unit=unit,
        vendor=vendor,
        catalog="UPADAPT",
    )
    order.add_item(item=item_1, n_units=10, cost_per_unit=20)
    order.add_item(item=item_2, n_units=1, cost_per_unit=200)

    a_order = Order.objects.with_counts().get(id=order.id)
    assert a_order.item_count == 2
    assert a_order.item_received_count == 0


@pytest.mark.django_db
def test_order_unplaced(sentinel_user):
    account = Account.objects.create(code="1234", description="unicorn paste fund")
    order = Order.objects.create(
        name="yearly unicorn paste supply", requested_by=sentinel_user
    )
    order.add_account(account)

    assert order in Order.objects.not_placed()
    assert order not in Order.objects.placed()
    assert order not in Order.objects.not_completed()
    assert order not in Order.objects.completed()


@pytest.mark.django_db
def test_order_placed(sentinel_user):
    account = Account.objects.create(code="1234", description="unicorn paste fund")
    order = Order.objects.create(
        name="yearly unicorn paste supply", requested_by=sentinel_user
    )
    order.add_account(account)
    order.mark_placed()

    assert order not in Order.objects.not_placed()
    assert order in Order.objects.placed()
    assert order not in Order.objects.not_completed()
    assert order in Order.objects.completed()


@pytest.mark.django_db
def test_order_completed(sentinel_user):
    category = Category.objects.create(name="glues and pastes")
    unit = Unit.objects.create(name="each")
    vendor = Vendor.objects.create(name="Unicorn Dispensary")
    account = Account.objects.create(code="1234", description="unicorn paste fund")
    order = Order.objects.create(
        name="yearly unicorn paste supply", requested_by=sentinel_user
    )
    order.add_account(account)

    item_1 = Item.objects.create(
        name="unicorn paste",
        category=category,
        unit=unit,
        vendor=vendor,
        catalog="UPASTE1",
    )
    item_2 = Item.objects.create(
        name="unicorn paste adapter",
        category=category,
        unit=unit,
        vendor=vendor,
        catalog="UPADAPT",
    )
    oitem_1 = order.add_item(item=item_1, n_units=10, cost_per_unit=20)
    oitem_2 = order.add_item(item=item_2, n_units=1, cost_per_unit=200)
    order.mark_placed()
    oitem_1.mark_arrived()
    oitem_2.mark_arrived()

    assert order not in Order.objects.not_placed()
    assert order in Order.objects.placed()
    assert order not in Order.objects.not_completed()
    assert order in Order.objects.completed()


@pytest.mark.django_db
def test_order_not_completed(sentinel_user):
    category = Category.objects.create(name="glues and pastes")
    unit = Unit.objects.create(name="each")
    vendor = Vendor.objects.create(name="Unicorn Dispensary")
    account = Account.objects.create(code="1234", description="unicorn paste fund")
    order = Order.objects.create(
        name="yearly unicorn paste supply", requested_by=sentinel_user
    )
    order.add_account(account)

    item_1 = Item.objects.create(
        name="unicorn paste",
        category=category,
        unit=unit,
        vendor=vendor,
        catalog="UPASTE1",
    )
    item_2 = Item.objects.create(
        name="unicorn paste adapter",
        category=category,
        unit=unit,
        vendor=vendor,
        catalog="UPADAPT",
    )
    oitem_1 = order.add_item(item=item_1, n_units=10, cost_per_unit=20)
    _oitem_2 = order.add_item(item=item_2, n_units=1, cost_per_unit=200)
    order.mark_placed()
    oitem_1.mark_arrived()

    assert order not in Order.objects.not_placed()
    assert order in Order.objects.placed()
    assert order in Order.objects.not_completed()
    assert order not in Order.objects.completed()


@pytest.mark.django_db
def test_order_with_multiple_accounts(sentinel_user):
    account1 = Account.objects.create(code="1234", description="fund 1")
    account2 = Account.objects.create(code="5678", description="fund 2")
    account3 = Account.objects.create(code="9101", description="fund 3")
    order = Order.objects.create(name="multi-account order", requested_by=sentinel_user)
    order.add_account(account1)
    order.add_account(account2)

    assert order.accounts.count() == 2
    assert account1 in order.accounts.all()
    assert account2 in order.accounts.all()
    assert account3 not in order.accounts.all()
    assert order in account1.orders.all()
    assert order in account2.orders.all()
    assert order not in account3.orders.all()
    assert order.account_codes() == "1234, 5678"
