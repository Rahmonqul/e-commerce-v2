# Generated by Django 5.1.4 on 2025-01-09 19:12

import django_ckeditor_5.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0020_remove_orderitem_shipping_servise_alter_order_adress'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banners',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200, null=True)),
                ('description', django_ckeditor_5.fields.CKEditor5Field(verbose_name='Text')),
                ('image', models.ImageField(blank=True, null=True, upload_to='banners/')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=300, null=True)),
                ('icon', models.ImageField(upload_to='')),
                ('subtitle', models.CharField(blank=True, max_length=1000, null=True)),
            ],
        ),
    ]
