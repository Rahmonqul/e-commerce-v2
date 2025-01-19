from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field
import uuid
from django.conf import settings
from hitcount.models import HitCountMixin, HitCount
from mptt.models import MPTTModel, TreeForeignKey
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from usauth import models as user_models
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
# Create your models here.

STATUS=(
    ('Published','Published'),
    ('Draft','Draft'),
    ('Disbled','Disbled')
)

PAYMENT_STATUS=(
    ('PENDING','PENDING'),
    ('PROCESSING','PROCESSING'),
    ('FAILED','FAILED')
)

PAYMENT_METHOD=(
    ('PayPal', 'PayPal'),
    ('Click', 'CLick'),
    ('Paynet', 'Paynet'),
)

ORDER_STATUS=(
    ('Pending','Pending'),
    ('Shipped', 'Shipped'),
    ('Cancelled', "Cancelled"),
)

SHIPPING_SERVISE=(
    ('DHL', 'DHL'),
)

RATING=(
    (1, '💛🤍🤍🤍🤍'),
    (2, '💛💛🤍🤍🤍'),
    (3, '💛💛💛🤍🤍'),
    (4, '💛💛💛💛🤍'),
    (5, '💛💛💛💛💛'),
)


class Category(MPTTModel):
    title=models.CharField(max_length=200, verbose_name='name category')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    image=models.ImageField(upload_to='category/', null=True, blank=True)
    slug=models.SlugField(unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural='Categories'
        ordering=['title']

class SubCategory(models.Model):
    title=models.CharField(max_length=200, verbose_name='name subcategory')
    image=models.ImageField(upload_to='subcategory/', null=True, blank=True)
    category=TreeForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    slug=models.SlugField(unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural='Subcategories'
        ordering=['title']


class Brand(models.Model):
    brand_name=models.CharField(max_length=200, null=True, blank=True)
    image=models.ImageField(upload_to='brands/', null=True, blank=True)

    def __str__(self):
        return self.brand_name

class Currency(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50)
    rate_to_usd = models.DecimalField(max_digits=10, decimal_places=4)

    def __str__(self):
        return f'{self.name} ({self.code})'

    @staticmethod
    def get_default_currency():
        return Currency.objects.get(code='USD')


# class Color(models.Model):
#     name=models.CharField(max_length=200)
#
#     def __str__(self):
#         return self.name
#
#
# class Size(models.Model):
#     name = models.CharField(max_length=200)
#
#     def __str__(self):
#         return self.name
#
#
# class Style(models.Model):
#     name = models.CharField(max_length=200)
#
#     def __str__(self):
#         return self.name



class Product(models.Model, HitCountMixin):
    name=models.CharField(max_length=200)
    image=models.ImageField(upload_to='product/',blank=True, null=True)
    description=CKEditor5Field('Description')
    additional_info=CKEditor5Field("Additional Info", blank=True, null=True)

    category=TreeForeignKey(Category, on_delete=models.CASCADE)
    # subcategory=models.ForeignKey(SubCategory, on_delete=models.CASCADE)

    price=models.DecimalField(max_digits=15, decimal_places=2, default=0.00, blank=True, null=True)
    regular_price=models.DecimalField(max_digits=15, decimal_places=2, default=0.00, blank=True, null=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, default=Currency.get_default_currency)
    stock=models.PositiveIntegerField(default=0, null=True, blank=True)
    shipping=models.DecimalField(max_digits=15, decimal_places=2, default=0.00, blank=True, null=True)

    status=models.CharField(choices=STATUS, max_length=200, default='Published')
    featured=models.BooleanField(default=False, verbose_name='Marketplace Featured')

    best_seller = models.BooleanField(default=False, verbose_name='Best Seller')
    sale = models.BooleanField(default=False, verbose_name='On Sale')
    new_arrival = models.BooleanField(default=False, verbose_name='New Arrival')

    vendor=models.ForeignKey(user_models.User, related_name='vendor_products', on_delete=models.CASCADE, limit_choices_to={'profile__user_type': 'Vendor'}, null=True, blank=True)

    brand=models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True)

    sku = models.UUIDField(default=uuid.uuid4,  unique=True, editable=False)
    slug=models.SlugField(null=True, blank=True)

    date=models.DateTimeField(default=timezone.now)

    class Meta:
        ordering=['-id']
        verbose_name_plural='Products'

    def __str__(self):
        return self.name

    def save(
        self,
        *args,
        **kwargs,
    ):
        if not self.slug:
            self.slug=slugify(self.name)+'-'+str(uuid.uuid4())[:2]
        super(Product, self).save(*args, **kwargs)

    @property
    def price_in_requested_currency(self):
        user = self.vendor.user if self.vendor else None
        profile = user.profile if user else None

        if profile and profile.currency:
            user_currency = profile.currency
            conversion_rate = self.get_currency_conversion_rate(self.currency, user_currency)
            return round(self.price * conversion_rate, 2)
        return self.price  # Если у пользователя нет профиля или валюты, возвращаем цену по умолчанию

    @property
    def regular_price_in_requested_currency(self):
        user = self.vendor.user if self.vendor else None
        profile = user.profile if user else None

        if profile and profile.currency:
            user_currency = profile.currency
            conversion_rate = self.get_currency_conversion_rate(self.currency, user_currency)
            return round(self.regular_price * conversion_rate, 2)
        return self.regular_price  # Если у пользователя нет профиля или валюты, возвращаем regular_price по умолчанию

    @property
    def discount_percentage(self):
        if self.regular_price and self.price and self.regular_price > self.price:
            discount = ((self.regular_price - self.price) / self.regular_price) * 100
            return round(discount)
        return 0

    def get_currency_conversion_rate(self, from_currency, to_currency):
        # Получаем курсы для валюты
        from_currency_obj = get_object_or_404(Currency, code=from_currency.code)
        to_currency_obj = get_object_or_404(Currency, code=to_currency.code)

        if from_currency_obj == to_currency_obj:
            return 1
        # Конвертация через курс к USD
        conversion_rate = from_currency_obj.rate_to_usd / to_currency_obj.rate_to_usd
        return conversion_rate

class Variant(models.Model):
    variant_choices=(
        ('Color', 'Color'),
        ('Size', 'Size'),
        ('Style', 'Style')
    )
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    name=models.CharField(max_length=1000, verbose_name='Variant name', choices=variant_choices, default=None)

    def items(self):
        return VariantItem.objects.filter(variant=self)

    def __str__(self):
        return self.name

class VariantItem(models.Model):
    variant=models.ForeignKey(Variant, on_delete=models.CASCADE, related_name='variant_items')
    title=models.CharField(max_length=1000, verbose_name='item title', null=True, blank=True)
    content=models.CharField(max_length=1000, verbose_name='content item', null=True, blank=True)

    def __str__(self):
        return self.variant.name

class Media(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    image=models.ImageField(upload_to='image/')
    media_id=models.UUIDField(default=uuid.uuid4,  unique=True, editable=False)

    def __str__(self):
        return f'{self.product.name}- image'

    class Meta:
        verbose_name_plural='Media'
        ordering=['-id']

class Cart(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    user=models.ForeignKey(user_models.User, on_delete=models.CASCADE, null=True, blank=True)
    qty=models.PositiveIntegerField(default=0, null=True, blank=True)
    price=models.DecimalField(max_digits=15, decimal_places=2, default=0.00, blank=True, null=True)
    subtotal_price=models.DecimalField(max_digits=15, decimal_places=2, default=0.00, blank=True, null=True)
    # shipping=models.DecimalField(max_digits=15, decimal_places=2, default=0.00, blank=True, null=True)
    total=models.DecimalField(max_digits=15, decimal_places=2, default=0.00, blank=True, null=True)
    size=models.CharField(max_length=100, blank=True, null=True)
    color=models.CharField(max_length=100, blank=True, null=True)
    date=models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.price = self.product.price
        self.subtotal_price = self.qty * self.price
        super(Cart, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.product.name}'

class Coupon(models.Model):
    vendor=models.ForeignKey(user_models.User, on_delete=models.CASCADE)
    code=models.CharField(max_length=100)
    discount=models.IntegerField(default=1)

    def __str__(self):
        return  self.code


class Order(models.Model):
    vendors=models.ManyToManyField(user_models.User, limit_choices_to={'profile__user_type': 'Vendor'}, blank=True)
    customer=models.ForeignKey(user_models.User, limit_choices_to={'profile__user_type': 'Customer'}, on_delete=models.CASCADE, related_name='customer', null=True, blank=True)
    subtotal_price = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, blank=True, null=True)
    shipping=models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    tax=models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    service_fee=models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    total=models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    payment_method=models.CharField(max_length=200, choices=PAYMENT_METHOD, default=None, blank=True, null=True)
    payment_status=models.CharField(max_length=200, choices=PAYMENT_STATUS, default='Processing')
    order_status=models.CharField(max_length=200, choices=ORDER_STATUS, default='Pending')
    initial_total=models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    saved=models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    adress=models.ForeignKey('customer.Address', on_delete=models.CASCADE, null=True, blank=True)

    coupons=models.ManyToManyField(Coupon, blank=True)
    order_id=models.UUIDField(default=uuid.uuid4,  unique=True, editable=False)
    payment_id=models.CharField(null=True, blank=True, max_length=1000)
    date=models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural="Order"
        ordering=['-date']

    def __str__(self):
        return str(self.order_id)

    def order_items(self):
        return OrderItem.objects.filter(order=self)

class OrderItem(models.Model):
    order=models.ForeignKey(Order, on_delete=models.CASCADE)
    order_status=models.CharField(max_length=200, choices=ORDER_STATUS, default='Pending')
    # shipping_servise=models.CharField(max_length=200, choices=SHIPPING_SERVISE, default=None)
    tracking_id=models.CharField(max_length=200, default=None, blank=True, null=True)

    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    qty=models.PositiveIntegerField(default=0, null=True, blank=True)
    size = models.CharField(max_length=100, blank=True, null=True)
    color = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, blank=True, null=True)
    subtotal_price = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, blank=True, null=True)
    shipping = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    tax = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    service_fee = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    initial_total = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    saved = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    coupon = models.ManyToManyField(Coupon, blank=True)
    applied_coupon=models.BooleanField(default=False)
    item_id=models.UUIDField(default=uuid.uuid4,  unique=True, editable=False)
    vendor=models.ForeignKey(user_models.User, on_delete=models.CASCADE)
    date=models.DateTimeField(default=timezone.now)

    def order_id(self):
        return f'{self.order.order_id}'

    def __str__(self):
        return str(self.item_id)

    class Meta:
        ordering=['-date']


class Review(models.Model):
    user=models.ForeignKey(user_models.User, on_delete=models.CASCADE,  null=True, blank=True)
    product=models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True, related_name='reviews')
    review=models.TextField()
    reply=models.TextField(null=True, blank=True, default="")
    rating=models.IntegerField(choices=RATING, default=None)
    active=models.BooleanField(default=False)
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} review on {self.product.name}'

class Question(models.Model):
    user = models.ForeignKey(user_models.User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="User")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='questions', verbose_name="Product")
    question_text = models.TextField(verbose_name="Question Text")
    # answer_text = models.TextField(null=True, blank=True, verbose_name="Answer Text")
    active = models.BooleanField(default=False, verbose_name="Is Active")
    date_asked = models.DateTimeField(auto_now_add=True, verbose_name="Date Asked")
    # date_answered = models.DateTimeField(null=True, blank=True, verbose_name="Date Answered")

    def __str__(self):
        return f"Question by {self.user.username} on {self.product.name}"

    class Meta:
        verbose_name_plural = "Questions"
        ordering = ['-date_asked']

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', verbose_name="Question")
    user = models.ForeignKey(user_models.User, on_delete=models.CASCADE, verbose_name="User")
    answer_text = models.TextField(verbose_name="Answer Text")
    date_answered = models.DateTimeField(auto_now_add=True, verbose_name="Date Answered")

    def __str__(self):
        return f"Answer by {self.user.username} on {self.question.product.name}"



class Banners(models.Model):
    title=models.CharField(max_length=200, null=True, blank=True)
    description=CKEditor5Field('Text')
    image=models.ImageField(upload_to='banners/', null=True, blank=True)
    link=models.URLField(max_length=200, blank=True, null=True)
    is_active=models.BooleanField(default=False)


    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.is_active:
            Banners.objects.filter(is_active=True).update(is_active=False)
            # if Banners.objects.filter(is_active=True).exists():
            #     raise ValidationError("There is already an active instance.")
        super().save(*args, **kwargs)


class Service(models.Model):
    title=models.CharField(max_length=300, null=True, blank=True)
    icon=models.ImageField()
    subtitle=models.CharField(max_length=1000, null=True, blank=True)

    def resize_icon(image_field):
        icon = Image.open(image_field)
        icon = icon.resize((100, 100))
        thumb_io = BytesIO()
        icon.save(thumb_io, format='JPEG')
        thumb_file = InMemoryUploadedFile(thumb_io, None, image_field.name, 'image/jpeg', thumb_io.tell(), None)
        return thumb_file


class Videos(models.Model):
    title=models.CharField(max_length=200, null=True, blank=True)
    description=CKEditor5Field('Text')
    video=models.FileField(upload_to='videos/', null=True, blank=True)
    link=models.URLField(max_length=200, blank=True, null=True)
    is_active=models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.is_active:
            Videos.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)




# class AdditionalInfo(models.Model):
#     text=CKEditor5Field("Text")
#     product=models.ForeignKey(Product, on_delete=models.CASCADE)
#     def __str__(self):
#         return str(self.id)
