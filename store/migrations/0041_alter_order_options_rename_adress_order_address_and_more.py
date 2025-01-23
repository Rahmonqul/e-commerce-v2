# Generated by Django 5.1.4 on 2025-01-21 09:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0040_alter_cart_options_remove_cart_color_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-date'], 'verbose_name_plural': 'Orders'},
        ),
        migrations.RenameField(
            model_name='order',
            old_name='adress',
            new_name='address',
        ),
        migrations.RemoveField(
            model_name='order',
            name='service_fee',
        ),
        migrations.RemoveField(
            model_name='order',
            name='shipping',
        ),
        migrations.RemoveField(
            model_name='order',
            name='tax',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='color',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='shipping',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='size',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='tax',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='variant',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(blank=True, limit_choices_to={'profile__user_type': 'Customer'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='order',
            name='subtotal_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=15),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='store.order'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=15),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='qty',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='subtotal_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=15),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='tracking_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='vendor',
            field=models.ForeignKey(limit_choices_to={'profile__user_type': 'Vendor'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
