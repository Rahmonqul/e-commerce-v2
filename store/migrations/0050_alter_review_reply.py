# Generated by Django 5.1.4 on 2025-01-19 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0049_alter_review_reply'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='reply',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
