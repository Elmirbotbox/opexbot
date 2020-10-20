from django.db import models
from django.utils import timezone
from django.conf import settings
from django.utils.translation import gettext_lazy as _
# Category model of menu


class Category(models.Model):
    # Relationships
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Category Details
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return _("%(id)s %(premises)s %(name)s") % {
            'id': self.id,
            'premises': self.owner,
            'name': self.name,
        }


class Product(models.Model):
    # Relationships
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    owner_category = models.ForeignKey(
        Category, on_delete=models.CASCADE)

    # Product Details
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    product_image = models.ImageField(
        upload_to="product_images", height_field=None, width_field=None, max_length=None)
    ingridients = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return _("%(id)s %(premises)s %(name)s") % {
            'id': self.id,
            'premises': self.owner,
            'name': self.name,
        }
