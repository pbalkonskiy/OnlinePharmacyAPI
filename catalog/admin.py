from django.contrib import admin

from catalog.models import Product, Category, Manufacturer


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "price",
        "brand",
        "amount",
        "is_in_stock",
    )
    list_filter = (
        "category",
        "brand",
        "price",
        "amount",
    )
    empty_value_display = "undefined"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "is_subcategory",
        "parent_title",
    )


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "country",
    )
    list_filter = (
        "country",
    )
    empty_value_display = "undefined"
