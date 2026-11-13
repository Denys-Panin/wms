import pytest

from apps.products.models import Category, Product


@pytest.fixture
def category(db):
    return Category.objects.create(name="Electronics", slug="electronics")


@pytest.fixture
def product(db, category):
    return Product.objects.create(
        sku="LEN-T14-001", name="Lenovo ThinkPad T14", category=category
    )
