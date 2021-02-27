# Generated by Django 3.0.8 on 2021-02-23 03:20

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0019_auto_20210215_1519'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='favorite',
            field=models.ManyToManyField(related_name='product_favorite', to=settings.AUTH_USER_MODEL),
        ),
    ]