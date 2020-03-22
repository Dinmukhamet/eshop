# Generated by Django 2.2.5 on 2020-03-21 23:33

import core.models
import core.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0073_auto_20200321_2330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(max_length=254, storage=core.storage.OverwriteStorage(), upload_to=core.models.upload_location),
        ),
    ]
