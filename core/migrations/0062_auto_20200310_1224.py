# Generated by Django 2.2.5 on 2020-03-10 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0061_remove_product_issomething'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slider',
            name='image',
            field=models.URLField(default='https://imgur.com/bY5YJhB', max_length=254),
        ),
    ]
