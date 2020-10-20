from .api import (
    WorkHourListView,
    WorkHourListUpdateView,
    ChangePasswordView,
    UserInfoUpdateView,
    CourierCreateView,
    CourierInfoUpdateView,
    CourierDeleteView,
    CourierList,
    GetUserDetail,
)
from django.urls import path

urlpatterns = [
    path('workHours/', WorkHourListView.as_view()),
    path('workHours_update/', WorkHourListUpdateView.as_view()),
    path('change_password/', ChangePasswordView.as_view()),
    path('user_info_update/', UserInfoUpdateView.as_view()),
    path('courier/create/', CourierCreateView.as_view()),
    path('courier/<pk>/update/', CourierInfoUpdateView.as_view()),
    path('courier/<pk>/delete/', CourierDeleteView.as_view()),
    path('get_courier/', CourierList.as_view()),
    path('user_info/', GetUserDetail.as_view()),
]
