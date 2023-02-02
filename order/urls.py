from django.http import HttpResponse
from django.urls import path


urlpatterns = [
    path('check/', lambda request: HttpResponse('OK')),
]
