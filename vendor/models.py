from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field
import uuid
from usauth.models import *

RATING=(
    (1, '💛🤍🤍🤍🤍'),
    (2, '💛💛🤍🤍🤍'),
    (3, '💛💛💛🤍🤍'),
    (4, '💛💛💛💛🤍'),
    (5, '💛💛💛💛💛'),
)

NOTIFICATION_TYPE=(
    ("New Order", "new Order"),
    ("New Review", "New Review"),
)

PAYMENT_METHOD=(
    ('PayPal', 'PayPal'),
    ('Click', 'CLick'),
    ('Paynet', 'Paynet'),
)

TYPE=(
    ('New order', 'New order'),
    ('Item shipped', 'Item shipped'),
    ('Item delivered', 'Item delivered'),
)

class Vendor(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'profile__user_type': 'Vendor'}, related_name='vendor')
    store_name=models.CharField(max_length=200, null=True, blank=True)
    image=models.ImageField(upload_to='vendor/', blank=True)
    description=models.TextField(null=True, blank=True)
    country=models.CharField(max_length=200, null=True, blank=True)
    vendor_id=models.UUIDField(default=uuid.uuid4,  unique=True, editable=False)
    date=models.DateTimeField(auto_now_add=True)
    slug=models.SlugField(null=True, blank=True)

    def __str__(self):
        return str(self.store_name)

    def save(self, *args, **kwargs):
        if self.slug=="" or self.slug==None:
            self.slug=slugify(self.store_name)
        super(Vendor, self).save(*args, **kwargs)

class Payout(models.Model):
    vendor=models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True)
    item=models.ForeignKey("store.OrderItem", on_delete=models.CASCADE, null=True, related_name='Payout')
    amount=models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    payout_id=models.UUIDField(default=uuid.uuid4,  unique=True, editable=False)
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.vendor

    class Meta:
        ordering=['-date']


class BankAccount(models.Model):
    vendor=models.OneToOneField(Vendor, on_delete=models.CASCADE, null=True)
    account_type=models.CharField(max_length=200, choices=PAYMENT_METHOD, blank=True, null=True)

    bank_name=models.CharField(max_length=200)
    account_number=models.CharField(max_length=200)
    account_name=models.CharField(max_length=200)
    bank_code=models.CharField(max_length=200)

    stripe_id=models.CharField(max_length=200, null=True, blank=True)
    paypal_adress=models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name_plural="Bank Account"

    def __str__(self):
        return self.bank_name


class Notifications(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='vendor_notification')
    type=models.CharField(max_length=200, choices=TYPE, default=None)
    order=models.ForeignKey('store.OrderItem', on_delete=models.CASCADE)
    seen=models.BooleanField(default=False)
    date=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural="Notifications"

    def __str__(self):
        return self.type

class StoreReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    store = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='storereviews')
    review = models.TextField()
    reply = models.TextField(blank=True, null=True)  # Ответ на отзыв
    rating = models.IntegerField(choices=RATING, default=None)
    active = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} review on {self.store.store_name}'


