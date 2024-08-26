# Generated by Django 5.0.3 on 2024-08-21 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vault', '0019_alter_vault_priority'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vault',
            name='priority',
            field=models.IntegerField(blank=True, choices=[(1, 'Low'), (2, 'Medium'), (3, 'High'), (4, 'Critical')], default=1, null=True),
        ),
    ]
