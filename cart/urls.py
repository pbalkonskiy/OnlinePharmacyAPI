from django.urls import path

from cart.views import (CartRetrieveDeleteAllPositionsView,
                        CartListUpdatePositionsView,
                        CartDeletePositionsView)


urlpatterns = [
    path("<int:pk>/", CartRetrieveDeleteAllPositionsView.as_view()),
    path("<int:pk>/edit/", CartListUpdatePositionsView.as_view()),
    path("<int:pk>/<slug:product__slug>/", CartDeletePositionsView.as_view()),
]
