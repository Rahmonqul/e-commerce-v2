# Generated by Django 5.1.4 on 2025-01-02 14:49

import django.db.models.deletion
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
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('mobile', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('country', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('state', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('city', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('address', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('zip_code', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Customer Address',
            },
        ),
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('New order', 'New order'), ('Item shipped', 'Item shipped'), ('Item delivered', 'Item delivered')], default=None, max_length=200)),
                ('seen', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Notifications',
            },
        ),
        migrations.CreateModel(
            name='Whishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Whishlist',
            },
        ),
    ]
