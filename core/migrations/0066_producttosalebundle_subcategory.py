# Generated by Django 2.2.5 on 2020-03-11 15:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0065_auto_20200311_1510'),
    ]

    operations = [
        migrations.AddField(
            model_name='producttosalebundle',
            name='subcategory',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.Subcategory'),
            preserve_default=False,
        ),
    ]