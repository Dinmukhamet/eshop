# Generated by Django 2.2.5 on 2020-01-28 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20200123_1717'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='purchasedproduct',
            options={'ordering': ['product']},
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='product_pics/None/no-img.jpg', upload_to=None),
        ),
    ]
