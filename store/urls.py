from django.urls import path
from . import views

urlpatterns = [
    path('products', views.ProductList.as_view()),

    path('products/<pk>', views.ProductDetailAPIView.as_view()),

    path('collections', views.collection_list),

    path('collections/<pk>', views.collection_detail, name='collection-detail'),
]
