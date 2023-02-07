from django.contrib import admin

from users.models import CommonUser, Customer, Employee

# Register your models here.

admin.site.register(CommonUser)
admin.site.register(Customer)
admin.site.register(Employee)

