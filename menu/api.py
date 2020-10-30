from rest_framework import viewsets, permissions
from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    DestroyAPIView,
    UpdateAPIView
)
from rest_framework.response import Response
from .serializers import CategorySerializer, ProductSerializer
from .models import Category, Product
from rest_framework.views import APIView
from django.conf import settings
from django.db.models import Count
User = settings.AUTH_USER_MODEL


class CategoryViewSet(viewsets.ModelViewSet):
    permissions_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# get user product
class ProductViewSet(viewsets.ModelViewSet):
    permissions_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


'''
# create product
class ProductCreateView(CreateAPIView):
    permissions_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
'''


# update existing product
class ProductUpdateView(UpdateAPIView):
    permissions_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(owner=self.request.user)


'''
class ProductDeleteView(DestroyAPIView):
    permissions_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(owner=self.request.user)

'''


# get product by Bot
class ProductListView(APIView):
    permissions_classes = [
        permissions.AllowAny
    ]

    def get(self, request, owner_category):
        try:
            products = Product.objects.filter(
                owner_category=owner_category, is_active=True)
            serializer = ProductSerializer(products, many=True, context={"request": request})
            response = {
                'success': True,
                'product_list': serializer.data
            }
        except:
            response = {
                'success': False,
            }
        return Response(response)


# get product detail by Bot
class ProductDetailView(APIView):
    permissions_classes = [
        permissions.AllowAny
    ]

    def get(self, request, pro_id):
        try:
            products = Product.objects.get(id=pro_id)
            serializer = ProductSerializer(products, many=False, context={"request": request})
            response = {
                'success': True,
                'product_data': serializer.data
            }
        except:
            response = {
                'success': False
            }
        return Response(response)

    
class CategoryProductListView(APIView):
    permissions_classes = [
        permissions.IsAuthenticated
    ]

    def get(self, request):
        category = Category.objects.filter(
            owner=self.request.user).annotate(Count('id'))
        ids = [dict(id=i.id, name=i.name, mehsul=ProductSerializer(
            Product.objects.filter(owner_category=i.id), many=True).data) for i in category]

        return Response(ids)
