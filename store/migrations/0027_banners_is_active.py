# Generated by Django 5.1.4 on 2025-01-13 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0026_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='banners',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
