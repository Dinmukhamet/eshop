# Generated by Django 2.2.5 on 2020-02-02 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20200201_2049'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='total_purchase',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='Hit',
        ),
    ]
