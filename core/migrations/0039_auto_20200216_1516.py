# Generated by Django 2.2.5 on 2020-02-16 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0038_auto_20200216_1343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.URLField(default='https://imgur.com/bY5YJhB', max_length=254),
        ),
        migrations.AlterField(
            model_name='slider',
            name='image',
            field=models.URLField(default='https://imgur.com/ bY5YJhB', max_length=254),
        ),
    ]
