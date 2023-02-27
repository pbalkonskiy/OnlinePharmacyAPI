from django.contrib import admin

from order.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "key",
        "customer_id",
        "numb_of_positions",
        "total_price",
        "created_at",
        "delivery_method",
        "payment_method",
        "payment_status",
        "is_paid",
        "in_progress",
        "closed",
    )
    list_filter = (
        "is_paid",
        "closed",
        "customer_id",
        "created_at",
        "payment_status",
        "delivery_method",
    )
    empty_value_display = "undefined"
