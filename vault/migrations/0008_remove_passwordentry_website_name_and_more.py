# Generated by Django 5.0.3 on 2024-08-16 09:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vault', '0007_passwordhistory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='passwordentry',
            name='website_name',
        ),
        migrations.RemoveField(
            model_name='passwordentry',
            name='website_url',
        ),
    ]
