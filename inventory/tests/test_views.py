# -*- mode: python -*-
import pytest

from django.urls import reverse

@pytest.mark.django_db
def test_index(client):
    response = client.get(reverse("inventory:index"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_order_list_at_desired_location(client):
    response = client.get("/inventory/orders/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_unplaced_order_list_at_desired_location(client):
    response = client.get("/inventory/orders/unplaced/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_incomplete_order_list_at_desired_location(client):
    response = client.get("/inventory/orders/incomplete/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_item_list_at_desired_location(client):
    response = client.get("/inventory/items/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_order_404_invalid_order(client):
    response = client.get(reverse("inventory:order", args=[1]))
    assert response.status_code == 404


@pytest.mark.django_db
def test_order_404_invalid_item(client):
    response = client.get(reverse("inventory:item", args=[1]))
    assert response.status_code == 404
