# Generated by Django 5.1.6 on 2025-02-14 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_remove_product_image_product_main_image_productimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='phone_number',
            field=models.CharField(default=1234, max_length=15),
        ),
    ]
