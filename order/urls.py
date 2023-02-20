from django.urls import path

from order.views import (OrderListView,
                         OrderRetrieveUpdateDeleteView)


urlpatterns = [
    path('<int:pk>/', OrderListView.as_view()),
    path('<int:pk>/<int:id>/', OrderRetrieveUpdateDeleteView.as_view()),
]
