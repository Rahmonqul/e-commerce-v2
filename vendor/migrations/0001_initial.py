# Generated by Django 5.1.4 on 2025-01-02 14:49

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store', '0004_alter_media_options_product_status'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('New order', 'New order'), ('Item shipped', 'Item shipped'), ('Item delivered', 'Item delivered')], default=None, max_length=200)),
                ('seen', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.orderitem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vendor_notification', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Notifications',
            },
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_name', models.CharField(blank=True, max_length=200, null=True)),
                ('image', models.ImageField(blank=True, upload_to='vendor/')),
                ('description', models.TextField(blank=True, null=True)),
                ('country', models.CharField(blank=True, max_length=200, null=True)),
                ('vendor_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='vendor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('payout_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Payout', to='store.orderitem')),
                ('vendor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='vendor.vendor')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_type', models.CharField(blank=True, choices=[('PayPal', 'PayPal'), ('Click', 'CLick'), ('Paynet', 'Paynet')], max_length=200, null=True)),
                ('bank_name', models.CharField(max_length=200)),
                ('account_number', models.CharField(max_length=200)),
                ('account_name', models.CharField(max_length=200)),
                ('bank_code', models.CharField(max_length=200)),
                ('stripe_id', models.CharField(blank=True, max_length=200, null=True)),
                ('paypal_adress', models.CharField(blank=True, max_length=200, null=True)),
                ('vendor', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='vendor.vendor')),
            ],
            options={
                'verbose_name_plural': 'Bank Account',
            },
        ),
    ]
