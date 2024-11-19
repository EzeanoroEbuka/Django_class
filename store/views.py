from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import IsAdminOrReadOnly
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend

from .filter import ProductFilter
from .models import Collection, Review, Cart, CartItem, Order

from rest_framework.pagination import PageNumberPagination
from .serializer import ProductSerializer, CollectionSerializer, CreateProductSerializer, CreateReviewSerializer, \
    ReviewSerializer, CartSerializer, CartItemSerializer, OrderSerializer, AddToCartSerializer, CreateCartSerializer, \
    UpdateCartItem, CreateOrderSerializer
from .models import Product
from .pagination import DefaultPageNumberPagination


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.prefetch_related('collection__product_set').all()
    filter_backends = [DjangoFilterBackend]
    filterSet_class = ProductFilter
    pagination_class = DefaultPageNumberPagination
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductSerializer
        elif self.request.method == 'POST':
            return CreateProductSerializer
        return ProductSerializer


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    pagination_class = PageNumberPagination


class ReviewViewSet(ModelViewSet):
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ReviewSerializer
        elif self.request.method == 'POST':
            return CreateReviewSerializer
        return ReviewSerializer


class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CartSerializer
        elif self.request.method == 'POST':
            return CreateCartSerializer
        return CreateCartSerializer


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk'])

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddToCartSerializer
        if self.request.method == 'PATCH':
            return UpdateCartItem
        return CartItemSerializer

    def get_serializer_context(self):
        return {"cart_id": self.kwargs['cart_pk']}


class OrderViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(customer_id=self.request.user.id)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        return OrderSerializer

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}


# class ProductList(ListCreateAPIView):
#     queryset = Product.objects.all()
#
#     def get_serializer_class(self):
#         if self.request.method == 'GET':
#             return ProductSerializer
#         elif self.request.method == 'POST':
#             return CreateProductSerializer
#
#
# class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer


#
# class CollectionListApiView(ListCreateAPIView):
#     queryset = Collection.objects.all()
#     serializer_class = CollectionSerializer
#
#
# class CollectionDetailApiView(RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.all()
#     serializer_class = CollectionSerializer
#


# def get_queryset(self):
#     return Product.objects.all()

#
# @api_view()
# def collection_list(request):
#     collections = Collection.objects.all()
#     serializer = CollectionSerializer(collections, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)
#
#
# @api_view()
# def collection_detail(request, pk):
#     collection = get_object_or_404(Collection, pk=pk)
#     serializer = CollectionSerializer(collection)
#     return Response(serializer.data, status=status.HTTP_200_OK)


#
# @api_view(['GET', 'POST'])
# def product_list(request):
#     if request.method == 'GET':
#         product = Product.objects.all()
#         serializer = ProductSerializer(product, many=True,  context={"request": request})
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif request.method == 'POST':
#         serializer = CreateProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#
# @api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     if request.method == 'GET':
#         serializer = ProductSerializer(product)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     if request.method == 'PUT':
#         serializer = CreateProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data,status= status.HTTP_202_ACCEPTED)
#     if request.method == 'DELETE':
#         product.delete()
#         return Response(data={"message": f"Product with {pk} deleted"}, status= status.HTTP_204_NO_CONTENT)
#
