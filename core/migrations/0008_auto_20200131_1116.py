# Generated by Django 2.2.5 on 2020-01-31 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_producthit_producthitinstance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producthitinstance',
            name='total_purchase',
        ),
        migrations.AlterField(
            model_name='producthit',
            name='isActive',
            field=models.BooleanField(default=True),
        ),
    ]
