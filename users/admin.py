from django.contrib import admin

from users.models import CommonUser, Customer, Employee


# Register your models here.

class CommonUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'patronymic', 'is_active', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name')
    list_editable = ('is_active', 'is_staff', 'first_name', 'last_name')
    list_filter = ('username', 'first_name',)
    empty_value_display = "undefined"


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'slug', 'user', 'position',)
    list_editable = ('position',)
    list_filter = ('user', 'position',)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'slug', 'telephone_number', 'cart')
    list_display_links = ('user',)
    list_editable = ('telephone_number',)

    list_filter = ('user', 'telephone_number', 'cart')


admin.site.register(CommonUser, CommonUserAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Employee, EmployeeAdmin)

