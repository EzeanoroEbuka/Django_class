from uuid import uuid4

from django.db import models
from  django.conf import settings


class Collection(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)

    description = models.CharField(max_length=255, null=False, blank=False)

    price = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False)

    inventory = models.PositiveSmallIntegerField()

    last_update = models.DateTimeField(auto_now=True)

    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)

    promotion = models.ManyToManyField('Promotion', related_name='+')

    def __self__(self):
        return f"{self.title} {self.price}"

    class Meta:
        ordering = ['title']


class Cart(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now=True)


class Order(models.Model):
    PAYMENT_STATUS = [
        ('P', 'Pending'),
        ('S', 'Success'),
        ('F', 'Failed'),
    ]

    place_at = models.DateTimeField(auto_now_add=True)

    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS, default='Pending')

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)


class CartItem(models.Model):
    quantity = models.PositiveSmallIntegerField()

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')

    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class OrderItem(models.Model):

    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='order_item')

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.PositiveSmallIntegerField()

    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Address(models.Model):
    phone_number = models.PositiveSmallIntegerField()

    street = models.CharField(max_length=255, blank=False)

    city = models.CharField(max_length=255, blank=False)

    state = models.CharField(max_length=255)

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Promotion(models.Model):
    discount = models.DecimalField(max_digits=6, decimal_places=2)

    product = models.ManyToManyField(Product, related_name='+')


class Review(models.Model):

    title = models.CharField(max_length=255, blank=False)

    content = models.TextField()

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='reviews')
