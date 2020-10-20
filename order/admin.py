from django.contrib import admin
from .models import (
    Client,
    OrderItem,
    BasketList,
    FavoriteList,
)


# Register your models here.
admin.site.register(Client)
admin.site.register(OrderItem)
admin.site.register(BasketList)
admin.site.register(FavoriteList)
