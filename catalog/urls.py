from django.urls import path

from catalog.views import (CatalogListView,
                           CatalogRetrieveUpdateDeleteView,
                           CatalogCreateItemView, RaitingListUpdateView)

urlpatterns = [
    path("", CatalogListView.as_view()),
    path("new/", CatalogCreateItemView.as_view()),
    path("<slug:slug>/", CatalogRetrieveUpdateDeleteView.as_view()),
    path("raiting/<slug:slug>", RaitingListUpdateView.as_view()),  # special url for raiting.
]
