from django.urls import path

from catalog.views import (CatalogListView,
                           CatalogRetrieveUpdateDeleteView,
                           CatalogCreateItemView)


urlpatterns = [
    path("", CatalogListView.as_view()),
    path("new/", CatalogCreateItemView.as_view()),
    path("<slug:slug>/", CatalogRetrieveUpdateDeleteView.as_view()),
]
