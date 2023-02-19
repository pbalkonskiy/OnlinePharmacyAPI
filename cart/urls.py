from django.urls import path

from cart.views import (CartRetrieveDeleteAllPositionsView,
                        CartListUpdatePositionsView,
                        CartDeletePositionsView)


urlpatterns = [
    path("<int:pk>/", CartRetrieveDeleteAllPositionsView.as_view()),
    path("<int:pk>/items/", CartListUpdatePositionsView.as_view()),
    path("<int:pk>/items/<slug:slug>/", CartDeletePositionsView.as_view()),
]
