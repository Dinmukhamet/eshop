# Generated by Django 2.2.5 on 2020-02-04 15:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_auto_20200204_1444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='price',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Product'),
        ),
    ]
