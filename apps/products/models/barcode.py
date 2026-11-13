from django.db import models


class ProductBarcode(models.Model):
    class BarcodeType(models.TextChoices):
        EAN13 = "EAN13", "EAN-13"
        UPC = "UPC", "UPC"
        CODE128 = "CODE128", "CODE 128"
        OTHER = "OTHER", "Other"

    product = models.ForeignKey(
        "products.Product",
        on_delete=models.PROTECT,
        related_name="barcodes",
    )

    barcode = models.CharField(max_length=128, unique=True)
    barcode_type = models.CharField(
        max_length=20, choices=BarcodeType.choices, default=BarcodeType.OTHER
    )
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-is_primary", "barcode"]
        constraints = [
            models.UniqueConstraint(
                fields=["product"],
                condition=models.Q(is_primary=True),
                name="unique_primary_barcode_per_product",
            ),
        ]

    def __str__(self):
        return self.barcode
