# Generated by Django 5.1.4 on 2025-01-21 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0041_alter_order_options_rename_adress_order_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='price_addition',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=15),
        ),
    ]
