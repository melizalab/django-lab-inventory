# -*- mode: python -*-
import datetime

import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from inventory.models import (
    Account,
    Category,
    Item,
    Manufacturer,
    Order,
    Unit,
    Vendor,
)


@pytest.fixture
def user(db):
    """Create a test user"""
    return User.objects.create_user(username="testuser", password="testpass")


@pytest.fixture
def category(db):
    """Create a test category"""
    return Category.objects.create(name="Test Category")


@pytest.fixture
def unit(db):
    """Create a test unit"""
    return Unit.objects.create(name="each")


@pytest.fixture
def vendor(db):
    """Create a test vendor"""
    return Vendor.objects.create(name="Test Vendor")


@pytest.fixture
def manufacturer(db):
    """Create a test manufacturer"""
    return Manufacturer.objects.create(name="Test Manufacturer")


@pytest.fixture
def item(db, vendor, manufacturer, category, unit):
    """Create a test item"""
    return Item.objects.create(
        name="Test Item",
        vendor=vendor,
        catalog="CAT123",
        manufacturer=manufacturer,
        manufacturer_number="MFG456",
        category=category,
        unit=unit,
        size=1.0,
    )


@pytest.fixture
def account(db):
    """Create a test account"""
    return Account.objects.create(
        code="TEST001",
        description="Test Account",
        expires_on=datetime.date.today() + datetime.timedelta(days=365),
    )


@pytest.mark.django_db
def test_index(client):
    response = client.get(reverse("inventory:index"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_order_list_at_desired_location(client):
    response = client.get(reverse("inventory:orders"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_unplaced_order_list_at_desired_location(client):
    response = client.get(reverse("inventory:unplaced-orders"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_incomplete_order_list_at_desired_location(client):
    response = client.get(reverse("inventory:incomplete-orders"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_item_list_at_desired_location(client):
    response = client.get(reverse("inventory:items"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_order_404_invalid_order(client):
    response = client.get(reverse("inventory:order", args=[1]))
    assert response.status_code == 404


@pytest.mark.django_db
def test_order_404_invalid_item(client):
    response = client.get(reverse("inventory:item", args=[1]))
    assert response.status_code == 404


@pytest.mark.django_db
def test_unplaced_orders_view_shows_only_unplaced_orders(client, user, account):
    """Test that the unplaced orders view only shows orders that have not been marked as placed"""
    # Create an unplaced order
    unplaced_order = Order.objects.create(
        name="Unplaced Order", requested_by=user, placed_on=None
    )
    unplaced_order.accounts.add(account)

    # Create a placed order
    placed_order = Order.objects.create(
        name="Placed Order", requested_by=user, placed_on=datetime.date.today()
    )
    placed_order.accounts.add(account)

    # Get the unplaced orders view
    response = client.get(reverse("inventory:unplaced-orders"))
    assert response.status_code == 200

    # Check that only the unplaced order appears in the view
    order_list = list(response.context["order_list"])
    assert unplaced_order in order_list
    assert placed_order not in order_list


@pytest.mark.django_db
def test_incomplete_orders_view_shows_only_incomplete_orders(
    client, user, item, account
):
    """Test that the incomplete orders view only shows orders that have been placed but not all items received"""
    # Create a complete order (all items received)
    complete_order = Order.objects.create(name="Complete Order", requested_by=user)
    complete_order.accounts.add(account)
    complete_order.add_item(item=item, n_units=2, cost_per_unit=10.00)
    complete_order.mark_placed()
    for order_item in complete_order.orderitem_set.all():
        order_item.mark_arrived()

    # Create an incomplete order (not all items received)
    incomplete_order = Order.objects.create(name="Incomplete Order", requested_by=user)
    incomplete_order.accounts.add(account)
    incomplete_order.add_item(item=item, n_units=1, cost_per_unit=10.00)
    incomplete_order.add_item(item=item, n_units=1, cost_per_unit=10.00)
    incomplete_order.mark_placed()
    # Mark only one item as arrived
    incomplete_order.orderitem_set.first().mark_arrived()

    # Create an unplaced order (should not appear)
    unplaced_order = Order.objects.create(name="Unplaced Order", requested_by=user)
    unplaced_order.accounts.add(account)
    unplaced_order.add_item(item=item, n_units=1, cost_per_unit=10.00)

    # Get the incomplete orders view
    response = client.get(reverse("inventory:incomplete-orders"))
    assert response.status_code == 200

    # Check that only the incomplete order appears in the view
    order_list = list(response.context["order_list"])
    assert incomplete_order in order_list
    assert complete_order not in order_list
    assert unplaced_order not in order_list


@pytest.mark.django_db
def test_export_items_csv_requires_login_and_returns_csv(client, user, item):
    """The export endpoint should require login and return a CSV with item data."""
    # Not logged in -> should redirect to login (302)
    response = client.get(reverse("inventory:export_items_csv"))
    assert response.status_code in (302, 401)

    # Login and try again
    client.login(username="testuser", password="testpass")
    response = client.get(reverse("inventory:export_items_csv"))
    assert response.status_code == 200
    assert response["Content-Type"] == "text/csv"
    assert "attachment; filename=" in response["Content-Disposition"]

    content = response.content.decode("utf-8")
    # Header row should be present
    assert "Description" in content
    # Item name should be present in CSV output
    assert "Test Item" in content
