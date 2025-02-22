# Generated by Django 5.1.4 on 2025-01-02 11:51

import django.db.models.deletion
import django.utils.timezone
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=15, null=True)),
                ('subtotal_price', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=15, null=True)),
                ('shipping', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=15, null=True)),
                ('total', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=15, null=True)),
                ('size', models.CharField(blank=True, max_length=100, null=True)),
                ('color', models.CharField(blank=True, max_length=100, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100)),
                ('discount', models.IntegerField(default=1)),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='image/')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subtotal_price', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=15, null=True)),
                ('shipping', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('tax', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('service_fee', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('payment_method', models.CharField(blank=True, choices=[('PayPal', 'PayPal'), ('Click', 'CLick'), ('Paynet', 'Paynet')], default=None, max_length=200, null=True)),
                ('payment_status', models.CharField(choices=[('PENDING', 'PENDING'), ('PROCESSING', 'PROCESSING'), ('FAILED', 'FAILED')], default='Processing', max_length=200)),
                ('order_status', models.CharField(choices=[('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Cancelled', 'Cancelled')], default='Pending', max_length=200)),
                ('initial_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('saved', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('order_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('payment_id', models.CharField(blank=True, max_length=1000, null=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('coupons', models.ManyToManyField(blank=True, to='store.coupon')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer', to=settings.AUTH_USER_MODEL)),
                ('vendors', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Order',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_status', models.CharField(choices=[('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Cancelled', 'Cancelled')], default='Pending', max_length=200)),
                ('shipping_servise', models.CharField(choices=[('DHL', 'DHL')], default=None, max_length=200)),
                ('tracking_id', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('qty', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('size', models.CharField(blank=True, max_length=100, null=True)),
                ('color', models.CharField(blank=True, max_length=100, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=15, null=True)),
                ('subtotal_price', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=15, null=True)),
                ('shipping', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('tax', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('service_fee', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('initial_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('saved', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('applied_coupon', models.BooleanField(default=False)),
                ('item_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('coupon', models.ManyToManyField(blank=True, to='store.coupon')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.TextField()),
                ('reply', models.TextField()),
                ('rating', models.IntegerField(choices=[(1, '💛🤍🤍🤍🤍'), (2, '💛💛🤍🤍🤍'), (3, '💛💛💛🤍🤍'), (4, '💛💛💛💛🤍'), (5, '💛💛💛💛💛')], default=None)),
                ('active', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='store.product')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000, verbose_name='Variant name')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
        ),
        migrations.CreateModel(
            name='VariantItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=1000, null=True, verbose_name='item title')),
                ('content', models.CharField(blank=True, max_length=1000, null=True, verbose_name='content item')),
                ('variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variant_items', to='store.variant')),
            ],
        ),
    ]
