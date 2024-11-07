from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet

from .models import Collection, Review, Cart
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from .serializer import ProductSerializer, CollectionSerializer, CreateProductSerializer, CreateReviewSerializer, \
    ReviewSerializer, CreateCartSerializer, CartSerializer
from .models import Product


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()

    # serializer_class = CreateProductSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductSerializer
        elif self.request.method == 'POST':
            return CreateProductSerializer
        return ProductSerializer


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer


class ReviewViewSet(ModelViewSet):
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ReviewSerializer
        elif self.request.method == 'POST':
            return CreateReviewSerializer
        return ReviewSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()

    # def get_queryset(self):
    #     customer = self.kwargs['customer_pk']
    #     return Cart.objects.filter(customer_id=customer)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CartSerializer
        elif self.request.method == 'POST':
            return CreateCartSerializer
        return CartSerializer



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
