from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field

from django.conf import settings

USER_TYPE=(
    ('Vendor', 'Vendor'),
    ('Customer', 'Customer')
)

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(max_length=250, null=True, blank=True)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.username:
            email_username, _ = self.email.split("@")
            self.username = email_username
        super(User,self).save(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user_profile/', null=True, blank=True)
    full_name = models.CharField(max_length=200, null=True, blank=True)
    mobile = models.CharField(max_length=200, null=True, blank=True)
    user_type = models.CharField(max_length=200, choices=USER_TYPE, null=True, blank=True, default=None)

    currency=models.ForeignKey('store.Currency', on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if not self.full_name:
            self.full_name = self.user.username
        super(Profile, self).save(*args, **kwargs)
