# Generated by Django 5.1.4 on 2025-01-02 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_media_media_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='media',
            options={'ordering': ['-id'], 'verbose_name_plural': 'Media'},
        ),
        migrations.AddField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('Published', 'Published'), ('Draft', 'Draft'), ('Disbled', 'Disbled')], default='Published', max_length=200),
        ),
    ]
