# Generated by Django 5.1.4 on 2025-01-11 15:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0024_product_currency'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='price',
        ),
    ]
