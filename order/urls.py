from django.urls import path

from order.views import (OrderActiveListView,
                         OrderClosedListView,
                         OrderRetrieveUpdateDeleteView,
                         OrderCheckOutView,
                         OrderBookingSetupView,
                         OrderBookingConfirmView, DeliveryConfirmView, DeliveryListView)


urlpatterns = [
    path("<int:pk>/", OrderActiveListView.as_view(), name="orders_active_url"),
    path("<int:pk>/closed/", OrderClosedListView.as_view(), name="orders_closed_url"),

    # Delivery-like order
    path("<int:pk>/<int:id>/", OrderRetrieveUpdateDeleteView.as_view(), name="order_retrieve_url"), #для создания заказа
    path("<int:pk>/<int:id>/checkout/", OrderCheckOutView.as_view(), name="checkout_url"), #для

    # Booking-like order
    path("<int:pk>/<int:id>/booking/", OrderBookingSetupView.as_view(), name="booking_ulr"),
    path("<int:pk>/<int:id>/booking/confirm/", OrderBookingConfirmView.as_view(), name="confirmation_url"),

    #Order management
    path("<int:pk>/<int:id>/manage/", DeliveryConfirmView.as_view(), name="order_manage_url"),
    path("<int:pk>/manage/", DeliveryListView.as_view(), name="list_of_customers_order"),

]
