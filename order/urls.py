from django.urls import path

from order.views import (OrderListView,
                         OrderRetrieveCheckOutDeleteView)


urlpatterns = [
    path('<int:pk>/', OrderListView.as_view()),
    path('<int:pk>/<int:id>/', OrderRetrieveCheckOutDeleteView.as_view()),
]
