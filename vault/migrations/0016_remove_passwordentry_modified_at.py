# Generated by Django 5.0.3 on 2024-08-18 15:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vault', '0015_passwordentry_updated_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='passwordentry',
            name='modified_at',
        ),
    ]
