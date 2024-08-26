# Generated by Django 5.0.3 on 2024-08-21 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vault', '0020_alter_vault_priority'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vault',
            name='priority',
            field=models.CharField(blank=True, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('critical', 'Critical')], default='low', max_length=15, null=True),
        ),
    ]
