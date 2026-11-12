from django.db import models


class Product(models.Model):
    class TrackingType(models.TextChoices):
        QUANTITY = "QUANTITY", "Quantity"
        SERIALIZED = "SERIALIZED", "Serialized"

    class Unit(models.TextChoices):
        PCS = "PCS", "Pieces"
        KG = "KG", "Kilograms"

    sku = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        "products.Category", on_delete=models.PROTECT, related_name="products"
    )
    description = models.TextField(blank=True)
    tracking_type = models.CharField(
        max_length=20, choices=TrackingType.choices, default=TrackingType.QUANTITY
    )
    unit = models.CharField(max_length=10, choices=Unit.choices, default=Unit.PCS)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.sku} - {self.name}"
