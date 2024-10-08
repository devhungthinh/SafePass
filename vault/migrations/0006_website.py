# Generated by Django 5.0.3 on 2024-08-16 04:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vault', '0005_alter_passwordentry_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('url', models.URLField()),
                ('password_entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vault.passwordentry')),
            ],
        ),
    ]
