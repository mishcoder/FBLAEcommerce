# Generated by Django 3.0.8 on 2021-02-25 03:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0025_size'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Size',
        ),
        migrations.RemoveField(
            model_name='product',
            name='large',
        ),
        migrations.RemoveField(
            model_name='product',
            name='medium',
        ),
        migrations.RemoveField(
            model_name='product',
            name='small',
        ),
    ]
