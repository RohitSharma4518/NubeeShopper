# Generated by Django 3.2 on 2022-03-20 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NubeeShopperApp', '0002_auto_20220315_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_image',
            field=models.ImageField(default='', upload_to='NubeeShopperApp/images'),
        ),
    ]