from pprint import pprint

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from . import views
from .views import OrderViewSet

route = DefaultRouter()
route.register('collections', views.CollectionViewSet, basename='collections')
route.register('products', views.ProductViewSet, basename='products')
route.register('carts', views.CartViewSet, basename='cart')
route.register('orders', views.OrderViewSet, basename='order')

product_route = NestedDefaultRouter(route, 'products', lookup='product')
product_route.register('reviews', views.ReviewViewSet, basename='product-review')

cart_item = NestedDefaultRouter(route, 'carts', lookup='cart')
cart_item.register('cart_items', views.CartItemViewSet, basename='cart_items')

urlpatterns = route.urls + product_route.urls + cart_item.urls


# pprint(urlpatterns)
# path('', include(route.urls)),
# path('', include(product_route.urls)),
# # path('', include(cart_item.urls)),
# ]

# path('products', views.ProductList.as_view()),
#
# path('products/<pk>', views.ProductDetailAPIView.as_view()),

# path('collections', views.CollectionListApiView.as_view()),
#
# path('collections/<pk>', views.CollectionDetailApiView.as_view()),
# ]
