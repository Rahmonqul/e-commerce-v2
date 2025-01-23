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

class Color(models.Model):
    name=models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Size(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Style(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name



class Product(models.Model, HitCountMixin):
    name=models.CharField(max_length=200)
    image=models.ImageField(upload_to='product/',blank=True, null=True)
    description=CKEditor5Field('Description')
    additional_info=CKEditor5Field("Additional Info", blank=True, null=True)

    category=TreeForeignKey(Category, on_delete=models.CASCADE)

    price=models.DecimalField(max_digits=15, decimal_places=2, default=0.00, blank=True, null=True)
    regular_price=models.DecimalField(max_digits=15, decimal_places=2, default=0.00, blank=True, null=True)

    # currency = models.ForeignKey(Currency, on_delete=models.CASCADE, default=None)
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


from decimal import Decimal




class Variant(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
        # name=models.CharField(max_length=1000, verbose_name='Variant name', choices=variant_choices, default=None)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, verbose_name='color', null=True, blank=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, verbose_name='Size', null=True, blank=True)
    style = models.ForeignKey(Style, on_delete=models.CASCADE, verbose_name='Style', null=True, blank=True)
    price_variant_field = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, blank=True, null=True)
    media = models.ImageField(null=True, blank=True)
    stock = models.IntegerField(null=True, blank=True)

    def __str__(self):
            return f'{self.product.name} color: {self.color}, style: {self.style}, size: {self.size}'

    def price_variant(self, user=None):
        if user and hasattr(user, 'profile') and user.profile.currency:
            conversion_rate = user.profile.currency.rate_to_usd
            if conversion_rate:
                return round(self.price_variant_field * conversion_rate, 2)

        return self.price_variant_field


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
    user = models.ForeignKey('usauth.User', on_delete=models.CASCADE, related_name='carts', null=True, blank=True)
    session_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"

    def __str__(self):
        return f"Cart {self.id} for {self.user.username if self.user else f'Anonymous {self.session_id}'}"

    @property
    def total_items(self):
        return self.items.aggregate(total=models.Sum('qty'))['total'] or 0

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

    def clear(self):
        self.items.all().delete()

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    variant = models.ForeignKey('Variant', on_delete=models.CASCADE, null=True, blank=True)
    qty = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"
        unique_together = ('cart', 'product', 'variant')

    def __str__(self):
        return f"{self.qty} x {self.product.name} (Variant: {self.variant if self.variant else 'N/A'})"

    @property
    def total_price(self):
        user = self.cart.user
        if self.variant:

            return self.variant.price_variant(user) * self.qty if user else self.variant.price_variant_field * self.qty
        return self.product.price * self.qty

    def update_qty(self, qty):
        self.qty = qty
        self.save()



class Coupon(models.Model):
    vendor=models.ForeignKey(user_models.User, on_delete=models.CASCADE)
    code=models.CharField(max_length=100)
    discount=models.IntegerField(default=1)

    def __str__(self):
        return  self.code



class Order(models.Model):
    vendors = models.ManyToManyField("usauth.User", limit_choices_to={'profile__user_type': 'Vendor'}, blank=True)
    customer = models.ForeignKey('usauth.User',  on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    subtotal_price = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    payment_method = models.CharField(max_length=200, choices=PAYMENT_METHOD, default=None, blank=True, null=True)
    payment_status = models.CharField(max_length=200, choices=PAYMENT_STATUS, default='Processing')
    order_status = models.CharField(max_length=200, choices=ORDER_STATUS, default='Pending')
    initial_total = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    saved = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    address = models.ForeignKey('customer.Address', on_delete=models.CASCADE, null=True, blank=True)
    coupons = models.ManyToManyField(Coupon, blank=True)
    order_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    payment_id = models.CharField(max_length=1000, null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)
    # cartitems=models.ManyToManyField("CartItem", blank=True)


    class Meta:
        verbose_name_plural = "Orders"
        ordering = ['-date']

    def __str__(self):
        return str(self.order_id)

    def order_items(self):
        return self.items.all()

    @property
    def total_items(self):
        return self.items.aggregate(total=models.Sum('qty'))['total'] or 0

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    order_status = models.CharField(max_length=200, choices=ORDER_STATUS, default='Pending')
    tracking_id = models.CharField(max_length=200, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    variant = models.CharField(max_length=200, blank=True, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    subtotal_price = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    service_fee = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    initial_total = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    saved = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    coupon = models.ManyToManyField(Coupon, blank=True)
    applied_coupon = models.BooleanField(default=False)
    item_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    vendor = models.ForeignKey('usauth.User', limit_choices_to={'profile__user_type': 'Vendor'}, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.item_id)

    class Meta:
        ordering = ['-date']



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
