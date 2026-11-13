from django.contrib import admin

from .models import Category, Product, ProductBarcode


@admin.register(ProductBarcode)
class ProductBarcodeAdmin(admin.ModelAdmin):
    list_display = (
        "barcode",
        "product",
        "barcode_type",
        "is_primary",
    )
    search_fields = ["barcode", "product__name", "product__sku"]
    list_filter = ("barcode_type", "is_primary")


admin.site.register(Category)
admin.site.register(Product)
