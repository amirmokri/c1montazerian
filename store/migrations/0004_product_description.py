# Generated by Django 5.1.6 on 2025-02-12 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_userprofile_delete_customuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.TextField(default='بهترین محصولات را از ما بخواهید.', max_length=2000),
        ),
    ]
