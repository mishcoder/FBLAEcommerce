# Generated by Django 3.0.8 on 2021-02-24 03:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0023_delete_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='stars',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
            preserve_default=False,
        ),
    ]
