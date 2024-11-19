import decimal
from decimal import Decimal
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from store.models import Product, Collection, Review, Cart, CartItem, Order, OrderItem
from user.models import Customer
from django.db import transaction


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


class CreateCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'created_at']


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


class AddToCartSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)
            return self.instance

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']


class UpdateCartItem(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']


class OrderItemSerializer(serializers.ModelSerializer):
    product = CartProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'unit_price', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    order_item = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'place_at', 'payment_status', 'customer', 'order_item']


class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.IntegerField()

    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data['cart_id']
            user_id = self.context['user_id']
            customer = get_object_or_404(Customer, id=user_id)
            order = Order.objects.create(customer=customer)
            cart_item = CartItem.objects.filter(cart_id=cart_id)

            order_items = [
                OrderItem(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    unit_price=item.product.price
                ) for item in cart_item
            ]
            OrderItem.objects.bulk_create(order_items)
            Cart.objects.get(id=cart_id).delete()
