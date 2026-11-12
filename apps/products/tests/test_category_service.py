import pytest
from django.core.exceptions import ValidationError

from apps.products.models import Category
from apps.products.services.category import change_category_parent


@pytest.mark.django_db
def test_change_category_parent():
    electronics = Category.objects.create(name="Electronics", slug="electronics")
    computers = Category.objects.create(name="Computers", slug="computers")
    change_category_parent(category=computers, new_parent=electronics)
    computers.refresh_from_db()
    assert computers.parent == electronics


@pytest.mark.django_db
def test_change_category_parent_to_none():
    electronics = Category.objects.create(name="Electronics", slug="electronics")
    computers = Category.objects.create(
        name="Computers", slug="computers", parent=electronics
    )
    change_category_parent(category=computers, new_parent=None)
    computers.refresh_from_db()
    assert computers.parent is None


@pytest.mark.django_db
def test_service_prevents_self_parent():
    electronics = Category.objects.create(name="Electronics", slug="electronics")
    with pytest.raises(ValidationError):
        change_category_parent(
            category=electronics,
            new_parent=electronics,
        )
    electronics.refresh_from_db()
    assert electronics.parent is None


@pytest.mark.django_db
def test_service_prevents_circular_relationship():
    electronics = Category.objects.create(name="Electronics", slug="electronics")
    computers = Category.objects.create(
        name="Computers", slug="computers", parent=electronics
    )
    laptops = Category.objects.create(name="Laptops", slug="laptops", parent=computers)
    with pytest.raises(ValidationError):
        change_category_parent(
            category=electronics,
            new_parent=laptops,
        )
    electronics.refresh_from_db()
    assert electronics.parent is None
