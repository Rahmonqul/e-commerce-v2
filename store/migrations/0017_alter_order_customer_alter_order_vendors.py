# Generated by Django 5.1.4 on 2025-01-09 08:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_remove_cart_shipping'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(blank=True, limit_choices_to={'profile__user_type': 'Customer'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='order',
            name='vendors',
            field=models.ManyToManyField(blank=True, limit_choices_to={'profile__user_type': 'Vendor'}, to=settings.AUTH_USER_MODEL),
        ),
    ]
