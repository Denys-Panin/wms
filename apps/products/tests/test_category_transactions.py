import pytest
from django.db import transaction

from apps.products.models import Category


@pytest.mark.django_db
def test_transaction_rollback():
    category = Category.objects.create(name="Electronics", slug="electronics")
    with pytest.raises(ValueError), transaction.atomic():
        category.name = "Updated Electronics"
        category.save(update_fields=["name"])

        raise ValueError("Something went wrong")

    category.refresh_from_db()
    assert category.name == "Electronics"
