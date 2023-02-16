from django.urls import path

from cart.views import CartRetrieveUpdateClearView


urlpatterns = [
    path("<int:pk>/", CartRetrieveUpdateClearView.as_view()),
]
