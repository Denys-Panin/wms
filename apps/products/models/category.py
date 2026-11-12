from django.core.exceptions import ValidationError
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=150)

    slug = models.SlugField(max_length=160, unique=True)
    parent = models.ForeignKey(
        "self", on_delete=models.PROTECT, related_name="children", null=True, blank=True
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        super().clean()

        if self.parent_id is None:
            return

        if self.pk is not None and self.parent_id == self.pk:
            raise ValidationError({"parent": "A category cannot be its own parent."})
        ancestor = self.parent
        visited = set()

        while ancestor is not None:
            if ancestor.pk == self.pk:
                raise ValidationError(
                    {"parent": "Circular category relationships are not allowed."}
                )
            visited.add(ancestor.pk)
            ancestor = ancestor.parent

    class Meta:
        ordering = ["name"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
