from rest_framework import mixins, permissions
from rest_framework import generics
from rest_framework import filters
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from django_filters import rest_framework

from django.http.response import Http404

from catalog.models import Product, Rating, Comments
from catalog.paginations import CatalogListPagination
from catalog.filters import ProductFilter
from catalog.serializers import (SimpleProductSerializer,
                                 ProductSerializer, RatingSerializer, CommentCustomerSerializer,
                                 CommentManagerSerializer)
from catalog.permissions import (IsCustomerOrReadOnly,
                                 IsStuffOrEmployeeOrReadOnly, IsStuffOrEmployee, IsProductManagerOrCustomet)

from cart.serializers import AddPositionSerializer
from users.models import CommonUser


class CatalogListView(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      generics.GenericAPIView):
    """
    View for browsing the catalog as a list of products.

    Also allows user to add products to the cart based on creating new positions using the POST
    request method. Required cart ID is set based on the ID of the user sending the requests.
    """
    queryset = Product.in_stock.all()  # Only in stock product are listed in catalog.

    serializer_class = SimpleProductSerializer
    pagination_class = CatalogListPagination
    permission_classes = (
        IsCustomerOrReadOnly,
    )

    # Filter parameters for 'django_filters.rest_framework'.
    filter_backends = (
        rest_framework.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filterset_class = ProductFilter

    # Search & ordering parameters for 'rest_framework.filters'.
    search_fields = ("^title",)
    ordering_fields = ("price",)
    ordering = ("-addition_date",)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Used to add new positions to the cart, in case the user is a customer,
        and he is signed in.
        """
        return self.create(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddPositionSerializer
        return self.serializer_class

    def get_serializer_context(self):
        """
        Adding the customer ID to the serializer context in case of "POST" request.
        """
        context = super(CatalogListView, self).get_serializer_context()
        if self.get_serializer_class() == AddPositionSerializer:
            context["user_id"] = self.request.user.customer.id
            context["product_id"] = self.request.data.get("product_id")
        return context


class CatalogRetrieveUpdateDeleteView(mixins.RetrieveModelMixin,
                                      mixins.UpdateModelMixin,
                                      mixins.DestroyModelMixin,
                                      generics.GenericAPIView):
    """
    View for retrieving one specific catalog item for observing;
    updating or deleting catalog items by administration.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "slug"
    permission_classes = (
        IsStuffOrEmployeeOrReadOnly,
    )

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CatalogCreateItemView(mixins.CreateModelMixin,
                            generics.GenericAPIView):
    """
    View for creating a new product.
    Originally allowed for resource administrations & managers stuff only.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    permission_classes = (
        IsStuffOrEmployee,
    )

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class RatingListUpdateView(mixins.RetrieveModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.UpdateModelMixin,
                           generics.GenericAPIView):
    queryset = Rating.objects.all()
    permission_classes = (
        IsCustomerOrReadOnly,
    )
    serializer_class = RatingSerializer
    lookup_field = "slug"

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            response = self.retrieve(request, *args, **kwargs)
        except Http404:
            data = {"Rating": "This product has no rating score yet"}
            response = Response(data=data, status=status.HTTP_404_NOT_FOUND)
        return response

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Http404:
            data = {"Rating": "This product has no rating score yet"}
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        my_model: Rating = self.get_object()
        user: CommonUser = request.user
        try:
            my_model.rating_set.pop(user.slug)
            my_model.save()
        except KeyError:
            raise NotFound("Object does not exist")
        else:
            return Response("Successfully deleted ")

    def get_object(self):
        queryset = self.get_queryset()
        obj = generics.get_object_or_404(queryset, slug=self.kwargs["slug"])
        return obj


class CustomCommentsView(generics.GenericAPIView,
                         mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin):
    lookup_field = "slug"
    serializer_class = CommentCustomerSerializer
    permission_classes = (IsProductManagerOrCustomet,)

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            print(self.request.method)
            return [IsCustomerOrReadOnly(), ]
        return [IsProductManagerOrCustomet(), ]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_queryset(self):
        product_id = Product.objects.filter(slug=self.kwargs["slug"]).first()

        if hasattr(self.request.user, 'employee') and self.request.user.employee.position == "content manager":
            return Comments.objects.filter(product=product_id, checked=False)

        elif self.request.method == "GET" or hasattr(self.request.user, 'customer'):
            return Comments.objects.filter(product=product_id, checked=True)

    def get_serializer_context(self):
        context = super(CustomCommentsView, self).get_serializer_context()
        context['slug'] = self.kwargs["slug"]
        return context

    def get_serializer_class(self):

        if hasattr(self.request.user, 'employee') and self.request.user.employee.position == "content manager":
            return CommentManagerSerializer

        elif self.request.method == "GET" or hasattr(self.request.user, 'customer'):
            return self.serializer_class
