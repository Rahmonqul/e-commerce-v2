# Generated by Django 5.1.4 on 2025-01-21 10:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0042_alter_cartitem_price_addition'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='variant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.variant'),
        ),
    ]
