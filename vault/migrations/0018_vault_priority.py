# Generated by Django 5.0.3 on 2024-08-21 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vault', '0017_passwordentry_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='vault',
            name='priority',
            field=models.IntegerField(blank=True, choices=[(1, 'Low'), (2, 'Medium'), (3, 'High'), (4, 'Critical')], null=True),
        ),
    ]
