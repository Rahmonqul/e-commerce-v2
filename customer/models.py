from django.db import models

from store.models import *
from usauth.models import *
# Create your models here.

TYPE=(
    ('New order', 'New order'),
    ('Item shipped', 'Item shipped'),
    ('Item delivered', 'Item delivered'),
)

class Whishlist(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural='Whishlist'

    def __str__(self):
        if self.product.name:
            return self.product.name
        else:
            return "Whishlist"

class Address(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE,  limit_choices_to={'profile__user_type': 'Customer'})
    full_name=models.CharField(max_length=200, null=True, blank=True, default=None)
    mobile=models.CharField(max_length=200, null=True, blank=True, default=None)
    country=models.CharField(max_length=200, null=True, blank=True, default=None)
    state=models.CharField(max_length=200, null=True, blank=True, default=None)
    city=models.CharField(max_length=200, null=True, blank=True, default=None)
    address=models.CharField(max_length=200, null=True, blank=True, default=None)
    zip_code=models.CharField(max_length=200, null=True, blank=True, default=None)

    class Meta:
        verbose_name_plural='Customer Address'

    def __str__(self):
        return self.full_name

class Notifications(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    type=models.CharField(max_length=200, choices=TYPE, default=None)
    seen=models.BooleanField(default=False)
    date=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural="Notifications"

    def __str__(self):
        return self.type

