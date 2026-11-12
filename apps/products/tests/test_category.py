import pytest
from django.core.exceptions import ValidationError
from django.db.models import ProtectedError

from apps.products.models import Category


@pytest.mark.django_db
def test_create_category():
    category = Category.objects.create(name="Electronics", slug="electronics")
    assert category.name == "Electronics"
    assert category.slug == "electronics"
    assert category.parent is None
    assert category.is_active is True


@pytest.mark.django_db
def test_create_subcategory():
    parent = Category.objects.create(name="Electronics", slug="electronics")
    child = Category.objects.create(name="Computers", slug="computers", parent=parent)
    assert child.parent == parent
    assert parent.children.count() == 1
    assert parent.children.first() == child


@pytest.mark.django_db
def test_cannot_delete_parent_with_children():
    parent = Category.objects.create(name="Electronics", slug="electronics")
    Category.objects.create(name="Computers", slug="computers", parent=parent)
    with pytest.raises(ProtectedError):
        parent.delete()


# @pytest.mark.django_db
# def test_category_cannot_be_its_own_parent():
#     category = Category.objects.create(name="Electronics", slug="electronics")
#     category.parent = category
#     with pytest.raises(ValidationError):
#         category.full_clean()
#
#
# @pytest.mark.django_db
# def test_category_cannot_create_cycle():
#     electronics = Category.objects.create(name="Electronics", slug="electronics")
#     computers = Category.objects.create(
#         name="Computers", slug="electronics", parent=electronics
#     )
#     laptops = Category.objects.create(name="Laptops", slug="laptops", parent=computers)
#     electronics.parent = laptos
#
#     with pytest.raises(ValidationError):
#         electronics.full_clean()


@pytest.mark.django_db
def test_category_cannot_be_its_own_parent():
    category = Category.objects.create(
        name="Electronics",
        slug="electronics",
    )

    category.parent = category

    with pytest.raises(ValidationError):
        category.full_clean()


@pytest.mark.django_db
def test_category_cannot_create_cycle():
    electronics = Category.objects.create(
        name="Electronics",
        slug="electronics",
    )

    computers = Category.objects.create(
        name="Computers",
        slug="computers",
        parent=electronics,
    )

    laptops = Category.objects.create(
        name="Laptops",
        slug="laptops",
        parent=computers,
    )

    electronics.parent = laptops

    with pytest.raises(ValidationError):
        electronics.full_clean()
