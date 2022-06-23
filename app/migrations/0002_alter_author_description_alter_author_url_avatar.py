# Generated by Django 4.0.5 on 2022-06-23 00:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='author',
            name='url_avatar',
            field=models.CharField(max_length=2049, null=True, validators=[django.core.validators.URLValidator()]),
        ),
    ]
