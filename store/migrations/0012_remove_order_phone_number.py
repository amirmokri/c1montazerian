# Generated by Django 5.1.6 on 2025-02-15 20:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_alter_userprofile_phone_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='phone_number',
        ),
    ]
