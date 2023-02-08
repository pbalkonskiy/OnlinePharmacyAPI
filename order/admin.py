from django.contrib import admin

from order.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "numb_of_positions",
        "total_price",
        "date",
        "delivery_method",
        "payment_method",
        "payment_status",
    )
    list_filter = (
        "date",
        "payment_status",
        "delivery_method",
    )
    empty_value_display = "undefined"
