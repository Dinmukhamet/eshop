# Generated by Django 2.2.5 on 2020-02-25 09:19

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0054_auto_20200225_0915'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='producttosale',
            options={'ordering': ['product']},
        ),
        migrations.RemoveField(
            model_name='producttosale',
            name='product',
        ),
        migrations.AddField(
            model_name='producttosale',
            name='product',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='category', chained_model_field='category', default=4, on_delete=django.db.models.deletion.CASCADE, to='core.Product'),
            preserve_default=False,
        ),
    ]