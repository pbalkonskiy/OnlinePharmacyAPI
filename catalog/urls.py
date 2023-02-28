from django.urls import path

from catalog.views import (CatalogListView,
                           CatalogRetrieveUpdateDeleteView,
                           CatalogCreateItemView, RatingListUpdateView)

urlpatterns = [
    path("", CatalogListView.as_view()),
    path("new/", CatalogCreateItemView.as_view()),
    path("<slug:slug>/", CatalogRetrieveUpdateDeleteView.as_view()),
    path("rating/<slug:slug>", RatingListUpdateView.as_view()),  # special url for rating.
]
