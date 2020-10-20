from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import WorkHour, Courier
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    DestroyAPIView,
    UpdateAPIView,
)
from .serializers import (
    WokrHoursSerializer,
    WorkHourUpdateSerializer,
    ChangePasswordSerializer,
    UserInfoUpdateSerializer,
    CourierSerializer,
    CourierListSerializer,
    UserSerializer,
)

from django.conf import settings
User = settings.AUTH_USER_MODEL


# User get workHours List
class WorkHourListView(ListAPIView):
    permissions_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = WokrHoursSerializer

    def get_queryset(self):
        return WorkHour.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# User Update workHours List
class WorkHourListUpdateView(UpdateAPIView):
    permissions_class = [
        permissions.IsAuthenticated,
    ]

    def get_object(self, obj_id):
        try:
            return WorkHour.objects.get(id=obj_id)
        except (WorkHour.DoesNotExist):
            raise status.HTTP_400_BAD_REQUEST

    def validate_ids(self, id_list):
        for id in id_list:
            try:
                WorkHour.objects.get(id=id)
            except (WorkHour.DoesNotExist):
                raise status.HTTP_400_BAD_REQUEST
        return True

    def put(self, request, *args, **kwargs):
        data = request.data
        ticket_ids = [i['id'] for i in data]
        self.validate_ids(ticket_ids)
        instances = []
        for temp_dict in data:
            ticket_id = temp_dict['id']
            weekday = temp_dict['weekday']
            to_hour = temp_dict['to_hour']
            from_hour = temp_dict['from_hour']
            is_active = temp_dict['is_active']
            obj = self.get_object(ticket_id)
            obj.weekday = weekday
            obj.to_hour = to_hour
            obj.from_hour = from_hour
            obj.is_active = is_active
            obj.save()
            instances.append(obj)
        serializer = WorkHourUpdateSerializer(instances, many=True)
        return Response(serializer.data)


# User Change Password
class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            if serializer.data.get("new_password") == serializer.data.get("renew_password"):
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Password updated successfully',
                    'data': []
                }

                return Response(response)

            elif serializer.data.get("new_password") != serializer.data.get("renew_password"):
                response = {
                    'status': 'fail',
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': 'Renew password are incorrect',
                    'data': []
                }
                return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# User update profile information
class UserInfoUpdateView(UpdateAPIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = UserInfoUpdateSerializer

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request):
        user = self.get_object
        try:
            user_serializer = UserInfoUpdateSerializer(
                request.user, data=request.data)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response(user_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'status': 0, 'message': 'Error on user update'})


class GetUserDetail(APIView):
    permissions = [
        permissions.IsAuthenticated
    ]
    serializer_class = UserSerializer

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def get(self, request):
        user = self.get_object
        user_serializer = UserSerializer(request.user)
        return Response(user_serializer.data, status=status.HTTP_200_OK)


# Courier Info Update by user(owner)1
class CourierInfoUpdateView(UpdateAPIView):
    permissions = (
        permissions.IsAuthenticated,
    )
    serializer_class = CourierSerializer

    def get_queryset(self):
        return Courier.objects.filter(owner=self.request.user)


#  Courier create by user(owner)
class CourierCreateView(CreateAPIView):
    permissions_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = CourierSerializer

    def get_queryset(self):
        return Courier.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# courier deleted by user(owner)
class CourierDeleteView(DestroyAPIView):
    permissions_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = CourierSerializer

    def get_queryset(self):
        return Courier.objects.filter(owner=self.request.user)


class CourierList(ListAPIView):
    permissions_classes = [
        permissions.IsAuthenticated,
    ]

    serializer_class = CourierListSerializer

    def get_queryset(self):
        return Courier.objects.filter(owner=self.request.user)
