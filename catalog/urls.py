from django.urls import path

from catalog.views import (CatalogListViewSet,
                           CatalogItemViewSet)


urlpatterns = [
    path("catalog/", CatalogListViewSet.as_view({"get": "list"})),
    path("catalog/<slug:slug>", CatalogItemViewSet.as_view({"get": "retrieve"})),
]
