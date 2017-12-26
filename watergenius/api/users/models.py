from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models

from api.properties.models import Property


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True, db_index=True, primary_key=True)
    USERNAME_FIELD = 'email'
    first_name = models.CharField(max_length=20, default="")
    last_name =models.CharField(max_length=20, default="")
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    props = models.ManyToManyField('Property', through='UserManagesProperty')
    objects = UserManager()

    def __str__(self):
        return 'email -> ' + self.email + ' Name -> ' + self.first_name + " " + self.last_name


class UserManagesProperty(models.Model):
    class Meta:
        unique_together = (('user_id', 'prop_id'),)
    user_id = models.ForeignKey(User, related_name='manager', on_delete=models.CASCADE)
    prop_id = models.ForeignKey(Property, related_name='prop', on_delete=models.CASCADE)