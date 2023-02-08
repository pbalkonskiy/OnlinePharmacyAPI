from django.contrib.auth.models import User, AbstractUser
from django.db import models

# from order.models import Order
from cart.models import Cart
from order.models import Order


class CommonUser(AbstractUser):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    patronymic = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(blank=True, null=True)


class Customer(models.Model):
    user = models.OneToOneField(CommonUser, related_name="customer", on_delete=models.CASCADE)
    telephone_number = models.CharField(max_length=20)
    cart = models.OneToOneField(Cart, related_name="customer", on_delete=models.CASCADE, null=True)
    order = models.ManyToManyField(Order, related_name="customer", null=True)


    class Meta:
        verbose_name = "customer"
        verbose_name_plural = "customers"

    def __str__(self):
        return self.user.first_name


class Employee(models.Model):
    user = models.OneToOneField(CommonUser, related_name="employee", on_delete=models.CASCADE)
    education = models.TextField(blank=True, null=True)
    position = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.user.first_name
