from django.urls import path, include, re_path

from users.views import CustomerViewList, CustomerRetrieveUpdateDeleteView, CustomerCreateView, EmployeeViewList, \
    EmployeeCreateView, EmployeeRetrieveUpdateDeleteView

urlpatterns = [
    path('customers/', CustomerViewList.as_view()),  # endpoint to get list of customers
    path('new_customer/', CustomerCreateView.as_view()),  # endpoint to create a new one customer
    path('customer/<slug:slug>/', CustomerRetrieveUpdateDeleteView.as_view()),  # endpoint to update or delete customer

    path('employees/', EmployeeViewList.as_view()),  # endpoint to get list of employees
    path('new_employee/', EmployeeCreateView.as_view()),  # endpoint to create a new
    path('employee/<slug:slug>/', EmployeeRetrieveUpdateDeleteView.as_view()),  # endpoint to update or delete employee

    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),  # authorization
    path('auth/', include('djoser.urls.jwt')),
    # path("api/accounts/", include("users.urls")),

]

#
# users endpoits (examples):
# http://127.0.0.1:8000/users/customers/ - list of all customers
# http://127.0.0.1:8000/users/new_customer/ - create a new customer
# http://127.0.0.1:8000/users/customer/user1@gmail.com - change/delete customer
#
# http://127.0.0.1:8000/users/employees/ - list of all employees
# http://127.0.0.1:8000/users/new_employee/ - create a new employee
# http://127.0.0.1:8000/users/employee/user1@gmail.com - change/delete employee
#
# http://127.0.0.1:8000/users/auth/users/ - list of all common users
# http://127.0.0.1:8000/users/auth/token/login - login by default token
# http://127.0.0.1:8000/users/auth/token/logout - logout by default token
# http://127.0.0.1:8000/users/auth/jwt/create - login by JWT token
# http://127.0.0.1:8000/users/auth/jwt/refresh - refresh JWT token
# http://127.0.0.1:8000/users/auth/jwt/verify - verify JWT token
