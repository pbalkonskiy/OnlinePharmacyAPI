from django.urls import path

from catalog.views import (CatalogListView,
                           CatalogItemView,
                           CatalogCreateItemView)


urlpatterns = [
    path("", CatalogListView.as_view()),
    path("new/", CatalogCreateItemView.as_view()),
    path("<slug:slug>/", CatalogItemView.as_view()),
]
