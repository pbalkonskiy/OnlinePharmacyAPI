from rest_framework import pagination


class CatalogListPagination(pagination.PageNumberPagination):
    """
    Pagination class for CatalogListViewSet.
    .../catalog/?limit=<'limit' value>
    """
    limit = 5
    page_size_query_param = "limit"
    max_page_size = 10_000
