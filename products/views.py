from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import action, api_view
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import ModelViewSet

from products.models import Sections, Brand, Product, Recall, Order
from products.permissions import IsAdminPermission
from products.serializers import SectionsSerializer, BrandSerializer, ProductListSerializer, RecallSerializer, \
    ProductSerializer


class SectionsListView(ListAPIView):
    queryset = Sections.objects.all()
    serializer_class = SectionsSerializer


class BrandListView(ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'slug'
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter,
                       filters.OrderingFilter]
    filterset_fields = ['brand__slug', 'section__slug']
    search_fields = ['title', 'brand__title', 'description']
    ordering_fields = ['title', 'price']

    @action(['GET'], detail=True)
    def recall(self, request, slug=None):
        product = self.get_object()
        recall = product.recalls.all()
        serializer = RecallSerializer(recall, many=True)
        return Response(serializer.data)

    @action(['POST'], detail=True)
    def order(self, request, slug=None):
        product = self.get_object()
        user = request.user
        try:
            order = Order.objects.get(product=product, user=user)
            order.is_ordered = not order.is_ordered
            order.save()
            message = 'Вы заказали' if order.is_ordered else 'Вы отменили заказ'
        except Order.DoesNotExist:
            Order.objects.create(product=product, user=user, is_ordered=True)
            message = 'Вы заказали'
        return Response(message, status=200)

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        return self.serializer_class

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permissions = [IsAdminPermission]
        elif self.action == 'order':
            permissions = [IsAuthenticated]
        else:
            permissions = []
        return [perm() for perm in permissions]


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'products': reverse('products-list', request=request, format=format),
        'brands': reverse('brands-list', request=request, format=format),
        'sections': reverse('sections-list', request=request, format=format),
    })


class RecallCreateView(CreateAPIView):
    queryset = Recall.objects.none()
    serializer_class = RecallSerializer
    permission_classes = [IsAuthenticated, ]


class BrandViewSet(ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    lookup_url_kwarg = 'slug'

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permissions = [IsAdminPermission]
        else:
            permissions = []
        return [perm() for perm in permissions]


class SectionsViewSet(ModelViewSet):
    queryset = Sections.objects.all()
    serializer_class = SectionsSerializer
    permission_classes = [IsAdminPermission, ]
    lookup_url_kwarg = 'slug'

