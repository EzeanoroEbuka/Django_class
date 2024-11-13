import decimal
from decimal import Decimal

from rest_framework import serializers
from store.models import Product, Collection, Review, Cart, CartItem


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title']


class ProductSerializer(serializers.ModelSerializer):
    # collection = serializers.HyperlinkedRelatedField(
    collection = CollectionSerializer()

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'inventory', 'price_with_discount', 'collection']

    price_with_discount = serializers.SerializerMethodField(method_name='discount')

    def discount(self, product: Product):
        return product.price * Decimal(0.01)


class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'price', 'description', 'inventory', 'collection']


class CreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['title', 'content', 'customer', 'product']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['title', 'content']


class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price']


class CartItemSerializer(serializers.ModelSerializer):
    product = CartProductSerializer()
    total_price = serializers.SerializerMethodField(
        method_name='get_total_price'
    )

    def get_total_price(self, cart_item: CartItem):
        return cart_item.product.price * cart_item.quantity

    class Meta:
        model = CartItem
        fields = ['id', 'quantity', 'product', 'total_price']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    total_price = serializers.SerializerMethodField(
        method_name='get_total_price'
    )

    def get_total_price(self, cart: Cart):
        # return sum(cart.items().all())
        return sum([item.quantity * item.product.price for item in cart.items.all()])

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']
