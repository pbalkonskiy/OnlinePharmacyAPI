from django.urls import path

from order.views import (OrderActiveListView,
                         OrderRetrieveUpdateDeleteView,
                         OrderCheckOutView)


urlpatterns = [
    path('<int:pk>/', OrderActiveListView.as_view(), name="orders_active_url"),
    path('<int:pk>/<int:id>/', OrderRetrieveUpdateDeleteView.as_view(), name="order_retrieve_url"),
    path('<int:pk>/<int:id>/checkout/', OrderCheckOutView.as_view(), name="checkout_url"),
]
