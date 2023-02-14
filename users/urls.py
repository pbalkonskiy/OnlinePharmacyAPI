from django.db import router
from django.http import HttpResponse
from django.urls import path, include, re_path

from users.views import CustomerViewList, CustomerRetrieveUpdateDeleteView, CustomerCreateView

urlpatterns = [
    path('check/', lambda request: HttpResponse('OK')),
    path('customers/', CustomerViewList.as_view()),  # endpoint to get list of customers
    path('new_customer/', CustomerCreateView.as_view()),  # endpoint to create a new one customer
    path('customer/<slug:slug>', CustomerRetrieveUpdateDeleteView.as_view()),  # endpoint to update or delete
]

"""
users endpoits:
http://127.0.0.1:8000/users/customer/user1@gmail.com
"""