from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.db import models

from .managers import UserManager


# Create your models here.
class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=11, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email', 'full_name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class OtpCode(models.Model):
    phone = models.CharField(max_length=11,unique=True)
    code = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}-{}-{}'.format(self.phone, self.code, self.created)
