# Generated by Django 3.0.8 on 2021-02-15 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0017_auto_20210215_1510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]
