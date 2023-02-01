from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('catalog/', include('catalog.urls')),
    path('cart/', include('cart.urls')),
    path('order/', include('order.urls')),
    path('users/', include('users.urls')),
]
