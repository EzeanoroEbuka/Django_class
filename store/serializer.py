import decimal
from decimal import Decimal

from rest_framework import serializers
from store.models import Product, Collection, Review, Cart


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title']


class ProductSerializer(serializers.ModelSerializer):
    # collection = serializers.HyperlinkedRelatedField(
    collection = CollectionSerializer()

    #     queryset=Collection.objects.all(), view_name='collection-detail'
    # )

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'Inventory', 'price_with_discount', 'collection']

    price_with_discount = serializers.SerializerMethodField(method_name='discount')

    def discount(self, product: Product):
        return product.price * Decimal(0.01)


class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'price', 'description', 'Inventory', 'collection']


class CreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['title', 'content', 'customer', 'product']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['title', 'content']


class CreateCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['customer']


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['created_at', 'customer']
