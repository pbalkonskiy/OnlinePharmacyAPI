from django.contrib import admin

from catalog.models import Product, Category, Manufacturer, Rating, Pharmacy, Comments


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "slug",
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


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "slug",
        "rating_set",
        "average_rating",
    )
    empty_value_display = "None"


@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product",
        "customer",
        "changed_at",
        "comment_field",
        "checked",
    )


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


@admin.register(Pharmacy)
class PharmacyAdmin(admin.ModelAdmin):
    list_display = (
        "address",
        "number",
        "opened_at",
        "closed_at",
        "is_opened",
    )
