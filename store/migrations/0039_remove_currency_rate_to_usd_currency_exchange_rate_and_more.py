# Generated by Django 5.1.4 on 2025-01-17 18:59

import django.db.models.deletion
import django.db.models.query
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0038_alter_variant_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='currency',
            name='rate_to_usd',
        ),
        migrations.AddField(
            model_name='currency',
            name='exchange_rate',
            field=models.DecimalField(decimal_places=6, default=1, max_digits=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='currency',
            field=models.ForeignKey(default=django.db.models.query.QuerySet.first, on_delete=django.db.models.deletion.CASCADE, to='store.currency'),
        ),
    ]
