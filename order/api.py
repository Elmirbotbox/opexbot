from django.utils import timezone
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import (
    Client,
    OrderItem,
    FavoriteList,
    BasketList,
)
from .serializers import (
    ClientSerializers,
    OrderItemSerializer,
    FavoriteListSerializer,
    BasketListSerializer,
)
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    DestroyAPIView,
    UpdateAPIView,
)
from menu.models import Product
from accounts.models import CustomUser, Courier


# ChatBot Side API
class Check_Client(APIView):
    permissions_classes = [
        permissions.AllowAny
    ]

    def get(self, request, name, surname, phone_number, fb_id):
        try:
            Client.objects.get(phone_number=phone_number)
            response = {
                'verified': True
            }
        except:
            Client.objects.create(name=name, surname=surname,
                                  phone_number=phone_number, fb_id=fb_id)
            response = {
                'verified': False
            }
        return Response(response)


class AddtoOrderItem(APIView):
    permissions_classes = [
        permissions.AllowAny
    ]

    def post(self, request, phone_number, product_id, quantity, owner):
        try:
            client_id = Client.objects.get(phone_number=phone_number)
            product_id = Product.objects.get(id=product_id, is_active=True)
            if OrderItem.objects.filter(client_id=client_id, product=product_id).exists():
                OrderItem.objects.filter(
                    client_id=client_id, product=product_id, is_ordered=False).update(quantity=quantity)
                response = {
                    'success': True,
                    'ststus': 'changed quantity',
                }
            else:
                OrderItem.objects.create(
                    client_id=client_id, product=product_id, quantity=quantity, owner=owner)
                response = {
                    'success': True,
                    'status': 'created',
                }
        except:
            response = {
                'success': False,
                'error': 404,
            }
        return Response(response)


class RemoveFromOrderItem(APIView):
    permissions_classes = [
        permissions.AllowAny
    ]

    def post(self, request, phone_number, product_id):
        try:
            client_id = Client.objects.get(phone_number=phone_number)
            OrderItem.objects.filter(
                client_id=client_id, product=product_id, is_ordered=False).delete()
            response = {
                'success': True,
                'status': 'removed OrderItem list'
            }
        except:
            response = {
                'success': False,
                'status': 'Not in the list.'
            }
        return Response(response)


class GetOrderItems(APIView):
    permissions_classes = [
        permissions.AllowAny
    ]

    def get(self, request, phone_number, owner):
        try:
            client_id = Client.objects.get(phone_number=phone_number)
            order_items = OrderItem.objects.filter(
                client_id=client_id, owner=owner, is_ordered=False)
            serializer = OrderItemSerializer(order_items, many=True)
            total = sum([i['final_price'] for i in serializer.data])
            response = {
                'success': True,
                'product_list': serializer.data,
                'final_total_price': format(total, '.2f')
            }
        except:
            response = {
                'success': False,
                'status': 'Not to find any items'
            }
        return Response(response)


class AddToFavoriteList(APIView):
    permissions_classes = [
        permissions.AllowAny
    ]

    def post(self, request, phone_number, product_id, owner):
        try:
            client_id = Client.objects.get(phone_number=phone_number)
            product = Product.objects.get(
                id=product_id, is_active=True, context={"request": request})
            if FavoriteList.objects.filter(client_id=client_id, product=product, owner=owner).exists():
                response = {
                    'success': 'False',
                    'status': 'already exists in favorite list.'
                }
            else:
                FavoriteList.objects.create(
                    client_id=client_id, product=product, owner=owner)
                response = {
                    'success': True,
                    'status': 'created',
                }
        except:
            response = {
                'success': False,
                'error': 404,
            }
        return Response(response)


class RemoveFromFavoriteList(APIView):
    permissions_classes = [
        permissions.AllowAny
    ]

    def post(self, request, phone_number, product_id):
        try:
            client_id = Client.objects.get(phone_number=phone_number)
            product_id = Product.objects.get(
                id=product_id, context={"request": request})
            FavoriteList.objects.filter(
                client_id=client_id, product_id=product_id).delete()
            response = {
                'success': True,
                'status': 'removed Favorite list.'
            }
        except:
            response = {
                'success': False,
                'error': 404,
            }
        return Response(response)


class GetFavoriteList(APIView):

    permissions_classes = [
        permissions.AllowAny,
    ]

    def get(self, request, phone_number, owner):
        try:
            client_id = Client.objects.get(phone_number=phone_number)
            favoriteList = FavoriteList.objects.filter(
                client_id=client_id, owner=owner)
            favorite = FavoriteListSerializer(
                favoriteList, many=True)
            return Response(favorite.data, status=status.HTTP_200_OK)
        except:
            response = {
                'success': False,
                'status': 'Not to find any items'
            }
            return Response(response)


class AddToBasketList(APIView):

    permissions_classes = [
        permissions.AllowAny,
    ]

    def post(self, request, phone_number, paymentType, deliveryType, owner):
        client_id = Client.objects.get(phone_number=phone_number)

        try:
            if BasketList.objects.filter(client_id=client_id, owner_id=owner, status=1).exists():
                response = {
                    'success': False,
                    'status': 'Already have orders in BasketList'
                }
            else:
                basketlist = BasketList.objects.create(
                    client_id=client_id, paymentType=paymentType, deliveryType=deliveryType, owner_id=owner)
                order_items = OrderItem.objects.filter(
                    client_id=client_id, is_ordered=False)
                for order_item in order_items:
                    basketlist.items.add(order_item)
                    order_item.save()
                response = {
                    'success': True,
                    'status': 'Orders add to Basket'
                }
        except:
            response = {
                'success': False,
                'status': 'error'
            }
        return Response(response)


class AddComment(APIView):

    permissions_classes = [
        permissions.AllowAny
    ]

    def put(self, request, phone_number, owner):
        client_id = Client.objects.get(phone_number=phone_number)
        try:
            if BasketList.objects.filter(client_id=client_id, owner_id=owner, status=1).exists():
                basket = BasketList.objects.filter(
                    client_id=client_id, owner_id=owner, status=1)
                data = request.data
                comment = data['comment']
                basket.update(comment=comment)
                response = {
                    'success': True,
                    'status': 'Comment added.'
                }
            else:
                response = {
                    'success': False,
                    'status': 'Not Have Order in BasketList'
                }
        except:
            response = {
                'success': False,
                'status': 'error'
            }
        return Response(response)


class TestingPayment(APIView):
    permissions_classes = [
        permissions.AllowAny
    ]

    def put(self, request, phone_number, owner):
        client_id = Client.objects.get(phone_number=phone_number)
        try:
            if BasketList.objects.filter(client_id=client_id, owner_id=owner, status=1).exists():
                basket = BasketList.objects.get(
                    client_id=client_id, owner_id=owner, status=1)
                ordered_items = basket.items.all()
                ordered_items.update(is_ordered=True)
                for item in ordered_items:
                    item.save()
                basket.status = 2
                basket.save()
                response = {
                    'success': True,
                    'status': 'Payment is successful.'
                }
            else:
                response = {
                    'success': False,
                    'status': 'some error'
                }
        except:
            response = {
                'success': False,
                'status': 'error'
            }
        return Response(response)


# User Side API
class IncomingList(ListAPIView):
    permissions_classes = [
        permissions.IsAuthenticated,
    ]

    serializer_class = BasketListSerializer

    def get_queryset(self):
        return BasketList.objects.filter(owner=self.request.user, status=2)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class IncomingToOutgoing(APIView):
    permissions_classes = [
        permissions.IsAuthenticated,
    ]

    def put(self, request, pk):
        try:
            basket = BasketList.objects.get(id=pk, owner=self.request.user)
            data = request.data
            if 'courier_id' and 'time' in data:
                if data['courier_id'] != "" and data['time'] != "":
                    courier = Courier.objects.get(id=data['courier_id'])
                    courier.assign_order.add(basket)
                    basket.time = data['time']
                    basket.save()
                elif data['courier_id'] != "" and data['time'] == "":
                    basket.time = data['time']
                    basket.save()
            basket.status = 3
            basket.being_delievered = timezone.now()
            basket.save()
            response = {
                'success': True
            }
        except:
            response = {
                'success': False,
                'status': 'error'
            }
        return Response(response)


class OutgoingList(ListAPIView):
    permissions_classes = [
        permissions.IsAuthenticated,
    ]

    serializer_class = BasketListSerializer

    def get_queryset(self):
        return BasketList.objects.filter(owner=self.request.user, status=3)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class OutgoingToReady(APIView):

    permissions_classes = [
        permissions.IsAuthenticated,
    ]

    def put(self, request, pk):
        basket = BasketList.objects.get(id=pk, owner=self.request.user)
        basket.status = 4
