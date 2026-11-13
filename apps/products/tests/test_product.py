import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

from apps.products.models import Category, Product


@pytest.fixture
def category(db):
    return Category.objects.create(name="Electronics", slug="electronics")


def test_create_product(category):
    product = Product.objects.create(
        sku="LEN-T14-001", name="Lenovo ThinkPad T14", category=category
    )

    assert product.sku == "LEN-T14-001"
    assert product.name == "Lenovo ThinkPad T14"
    assert product.category == category
    assert product.tracking_type == Product.TrackingType.QUANTITY
    assert product.unit == Product.Unit.PCS
    assert product.is_active is True


def test_product_sku_must_be_unique(category):
    Product.objects.create(sku="LEN-T14-001", name="Another laptop", category=category)

    with pytest.raises(IntegrityError), transaction.atomic():
        Product.objects.create(
            sku="LEN-T14-001",
            name="Another laptop",
            category=category,
        )


def test_category_reverse_relationship(category):
    Product.objects.create(
        sku="PRODUCT-001",
        name="Laptop",
        category=category,
    )

    Product.objects.create(
        sku="PRODUCT-002",
        name="Monitor",
        category=category,
    )

    assert category.products.count() == 2


def test_create_serialized_product(category):
    product = Product.objects.create(
        sku="LEN-T14-002",
        name="Lenovo ThinkPad T14",
        category=category,
        tracking_type=Product.TrackingType.SERIALIZED,
    )

    assert product.tracking_type == Product.TrackingType.SERIALIZED
    assert product.unit == Product.Unit.PCS


def test_serialized_product_requires_pcs(category):
    product = Product(
        sku="LEN-T14-003",
        name="Lenovo ThinkPad T14",
        category=category,
        tracking_type=Product.TrackingType.SERIALIZED,
        unit=Product.Unit.KG,
    )

    with pytest.raises(ValidationError) as exc_info:
        product.full_clean()

    assert "unit" in exc_info.value.message_dict


def test_database_reject_serialized_kg(category):
    with pytest.raises(IntegrityError), transaction.atomic():
        Product.objects.create(
            sku="LEN-T14-004",
            name="Laptop ThinkPad T14",
            category=category,
            tracking_type=Product.TrackingType.SERIALIZED,
            unit=Product.Unit.KG,
        )
