# Generated by Django 2.2.5 on 2020-02-23 15:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0044_auto_20200222_0840'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recommendedproduct',
            name='products',
        ),
        migrations.CreateModel(
            name='ProductToRecommendedProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Product')),
                ('recommended_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='core.RecommendedProduct')),
            ],
            options={
                'ordering': ['recommended_product'],
            },
        ),
    ]
