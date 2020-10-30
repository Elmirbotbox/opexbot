from rest_framework import routers
from django.urls import path
from .api import (
    CategoryViewSet,
    ProductViewSet,
    # ProductCreateView,
    # ProductDeleteView,
    ProductUpdateView,
    ProductListView,
    ProductDetailView,
)


router = routers.DefaultRouter()
router.register('categories', CategoryViewSet, 'category')
router.register('products', ProductViewSet, 'products')

urlpatterns = router.urls


urlpatterns = [
    path('categories/', CategoryViewSet.as_view({'get': 'list'})),
    path('products/', ProductViewSet.as_view({'get': 'list'})),
    path('get_products&cat_id=<owner_category>',
         ProductListView.as_view()),
    path('get_products&id=<pro_id>', ProductDetailView.as_view()),
    # path('products/create/', ProductCreateView.as_view()),
    path('products/<pk>/update/', ProductUpdateView.as_view()),
    # path('products/<pk>/delete/', ProductDeleteView.as_view())
    path('get/', CategoryProductListView.as_view()),
]
