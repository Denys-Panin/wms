from django.db import transaction

from apps.products.models import Category


@transaction.atomic
def change_category_parent(
    *, category: Category, new_parent: Category | None
) -> Category:
    list(
        Category.objects.order_by("pk").select_for_update().values_list("pk", flat=True)
    )
    category = Category.objects.get(pk=category.pk)
    parent = None

    if new_parent is not None:
        parent = Category.objects.get(pk=new_parent.pk)

    category.parent = parent
    category.full_clean()
    category.save(update_fields=["parent"])
    return category
