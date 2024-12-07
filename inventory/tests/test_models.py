# -*- mode: python -*-

import pytest
from django.contrib.auth import get_user_model

from inventory.models import Account, Category, Item, Order, OrderItem, Unit, Vendor


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username="deleted")[0]

@pytest.mark.django_db
def test_order_cost():
    user = get_sentinel_user()
    category = Category.objects.create(name="glues and pastes")
    unit = Unit.objects.create(name="each")
    vendor = Vendor.objects.create(name="Unicorn Dispensary")
    account = Account.objects.create(code="1234", description="unicorn paste fund")
    item = Item.objects.create(name="unicorn paste", category=category, unit=unit, vendor=vendor, catalog="UPASTE1")
    order = Order.objects.create(name="yearly unicorn paste supply", account=account, ordered_by=user)

    orderitem = OrderItem.objects.create(item=item, order=order, units_purchased=10, cost=20)

    assert orderitem.total_price() == 200
