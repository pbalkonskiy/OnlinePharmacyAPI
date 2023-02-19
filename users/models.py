from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

# from order.models import Order
from cart.models import Cart
from users.constants import POSITION


class CommonUser(AbstractUser):
    username = models.CharField(_("username"), max_length=30, null=True, blank=True, default=None, unique=False)
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    patronymic = models.CharField(max_length=150, null=True, blank=True)
    last_login = models.DateTimeField(_("last login"), blank=True, null=True, auto_now=True)
    slug = models.SlugField(max_length=150, unique=True, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name')

    def __str__(self)->str:
        return f"{self.slug}"

    def save(self, *args, **kwargs):
        slug_data = self.email.split('@')[0]
        self.slug = slugify(slug_data)
        return super(CommonUser, self).save(*args, **kwargs)


class Customer(models.Model):
    user = models.OneToOneField(CommonUser, related_name="customer", on_delete=models.CASCADE, null=True)
    slug = models.SlugField(max_length=150, unique=True, null=True, blank=True)
    telephone_number = models.CharField(max_length=20)
    cart = models.OneToOneField(Cart, related_name="customer", on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "customer"
        verbose_name_plural = "customers"

    def __str__(self)->str:
        return f"{self.slug}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.slug)
        return super(Customer, self).save(*args, **kwargs)


class Employee(models.Model):
    user = models.OneToOneField(CommonUser, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=150, unique=True, null=True, blank=True)
    education = models.TextField(blank=True, null=True)
    position = models.CharField(choices=POSITION, max_length=50)

    class Meta:
        verbose_name_plural = "employees"
        verbose_name = "employee"

    def __str__(self)->str:
        return f"{self.slug}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.slug)
        return super(Employee, self).save(*args, **kwargs)
