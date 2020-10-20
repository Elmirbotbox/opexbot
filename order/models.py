from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from datetime import date


class Client(models.Model):
    name = models.CharField(max_length=40, null=True)
    surname = models.CharField(max_length=56, null=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(
        validators=[phone_regex], max_length=17, blank=True)
    fb_id = models.CharField(max_length=765, blank=True, null=True)
    adress = models.TextField(null=True, default=True)


class BasketList(models.Model):

    Status = [
        (0, _("Rejected")),
        (1, _("Waiting Payment")),
        (2, _("Waiting Incoming")),
        (3, _("Accepted (Outgoing)")),
        (4, _("Being_Delivered(Ready)")),
        (5, _("Completed")),
    ]

    TypeOfPayment = [
        (1, _("Card")),
        (2, _("Cash")),
    ]

    DeliveryType = [
        (1, _("Delivery")),
        (2, _("Pick up")),
    ]

    id = models.BigAutoField(primary_key=True)
    daily_id = models.CharField(
        max_length=5, default=None, null=True, blank=True)
    client_id = models.ForeignKey(
        'Client', on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)
    items = models.ManyToManyField('OrderItem')
    status = models.IntegerField(_('status'), choices=Status, default=1)
    deliveryType = models.IntegerField(_('DeliveryType'), choices=DeliveryType)
    paymentType = models.IntegerField(
        _('PaymnetType'), choices=TypeOfPayment, default=1)
    time = models.IntegerField(default=25)
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    being_delievered = models.DateTimeField(blank=True, null=True)
    received = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.daily_id:
            prev_instances = self.__class__.objects.filter(
                created_at__month=date.today().month, owner=self.owner)
            if prev_instances.exists():
                last_id = prev_instances.last().daily_id
                if int(last_id) >= 1000:
                    self.daily_id = int(last_id)+1
                else:
                    self.daily_id = '{0:03d}'.format(int(last_id)+1)
            else:
                self.daily_id = '{0:03d}'.format(1)
        super(BasketList, self).save(*args, **kwargs)

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return format(total, '.2f')


class OrderItem(models.Model):
    client_id = models.ForeignKey(
        'Client', on_delete=models.CASCADE)
    product = models.ForeignKey('menu.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    is_ordered = models.BooleanField(default=False)
    owner = models.IntegerField()

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    def get_final_price(self):
        return self.quantity * self.product.price


class FavoriteList(models.Model):
    client_id = models.ForeignKey('Client', on_delete=models.CASCADE)
    product = models.ForeignKey("menu.Product", on_delete=models.CASCADE)
    owner = models.IntegerField()
