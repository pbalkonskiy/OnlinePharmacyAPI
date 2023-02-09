from django.contrib import admin

from cart.models import Position, Cart

class CartAdmin(admin.ModelAdmin):
    list_display = ('status', 'numb_of_positions', 'total_price')
    list_filter = ('status',)

class PositionAdmin(admin.ModelAdmin):
    list_display = ('product', 'amount', 'price')
    list_filter = ('product', 'amount')
    list_editable = ('amount',)
    search_fields = ('amount',)

admin.site.register(Position, PositionAdmin)
admin.site.register(Cart, CartAdmin)
# Register your models here.
