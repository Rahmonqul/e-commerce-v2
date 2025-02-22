# Generated by Django 5.1.4 on 2025-01-05 18:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='StoreReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.TextField()),
                ('reply', models.TextField(blank=True, null=True)),
                ('rating', models.IntegerField(choices=[(1, '💛🤍🤍🤍🤍'), (2, '💛💛🤍🤍🤍'), (3, '💛💛💛🤍🤍'), (4, '💛💛💛💛🤍'), (5, '💛💛💛💛💛')], default=None)),
                ('active', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='storereviews', to='vendor.vendor')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
