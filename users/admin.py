from django.contrib import admin

from users.models import CommonUser, Customer

# Register your models here.

admin.site.register(CommonUser)
admin.site.register(Customer)
