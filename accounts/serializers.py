from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import WorkHour, Courier
User = get_user_model()


'''
class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'name', 'password')
'''


class UserSerializer(UserCreateSerializer):
    profile_url = serializers.SerializerMethodField()

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'name', 'surname', 'password',
                  'profile_image', 'profile_url', 'username')

    def get_profile_url(self, obj):
        request = self.context.get('request')
        if obj.profile_image:
            photo_url = obj.profile_image.url
            return request.build_absolute_uri(photo_url)
        else:
            return 'no image'


class UserInfoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'surname', 'username', 'profile_image')


class WokrHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkHour
        fields = '__all__'


class WorkHourUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkHour
        fields = ('id', 'weekday', 'from_hour', 'to_hour', 'is_active')


class CourierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courier
        fields = ('name', 'surname', 'phone_number', 'is_active')


class CourierListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courier
        fields = ('id', 'name', 'surname', 'phone_number', 'is_active')


class ChangePasswordSerializer(serializers.Serializer):
    class Meta:
        model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    renew_password = serializers.CharField(required=True)
