from django.urls import path

from cart.views import (CartRetrieveClearView,
                        CartUpdateView)


urlpatterns = [
    path("<int:pk>/", CartRetrieveClearView.as_view()),
    path("<int:pk>/items/", CartUpdateView.as_view()),
]
