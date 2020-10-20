from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.validators import RegexValidator

from order.models import BasketList


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    # CustomUser details ... (In future versions,  Admin User Panel)
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(max_length=56, null=True)
    surname = models.CharField(max_length=56, null=True)
    username = models.CharField(max_length=56, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    profile_image = models.ImageField(
        upload_to='profile_images', height_field=None, width_field=None, max_length=None)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class WorkHour(models.Model):
    WEEKDAYS = [
        (1, _("Bazar ertəsi")),
        (2, _("Cərşənbə axşamı")),
        (3, _("Çərşənbə")),
        (4, _("Cümə axşamı")),
        (5, _("Cümə")),
        (6, _("Şənbə")),
        (7, _("Bazar")),
    ]
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    weekday = models.IntegerField(_('Weekday'), choices=WEEKDAYS)
    from_hour = models.TimeField(_('Opening'))
    to_hour = models.TimeField(_('Closing'))
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return _("%(weekday)s %(premises)s (%(from_hour)s - %(to_hour)s)") % {
            'premises': self.owner,
            'weekday': self.weekday,
            'from_hour': self.from_hour,
            'to_hour': self.to_hour
        }

    class Meta:
        unique_together = (('owner', 'weekday'))


class Courier(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=56, null=True)
    surname = models.CharField(max_length=56, null=True)
    is_active = models.BooleanField(default=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(
        validators=[phone_regex], max_length=17, blank=True)
    assign_order = models.ManyToManyField(
        BasketList, blank=True)

    def __str__(self):
        return _("%(premises)s %(phone_number)s") % {
            'premises': self.owner,
            'phone_number': self.phone_number,
        }
