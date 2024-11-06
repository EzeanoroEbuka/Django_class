from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from . import views

route = DefaultRouter()
route.register('collections', views.CollectionViewSet, basename='collections')
route.register('products', views.ProductViewSet, basename='products')

product_route = NestedDefaultRouter(route, 'products', lookup='product')
product_route.register('reviews', views.ReviewViewSet, basename='product-review')

urlpatterns = route.urls + product_route.urls

# urlpatterns = [
#
#     path('', include(route.urls)),
#     path('', include(product_route)),

# path('products', views.ProductList.as_view()),
#
# path('products/<pk>', views.ProductDetailAPIView.as_view()),

# path('collections', views.CollectionListApiView.as_view()),
#
# path('collections/<pk>', views.CollectionDetailApiView.as_view()),
# ]
