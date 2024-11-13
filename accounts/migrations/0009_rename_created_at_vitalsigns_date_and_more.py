# Generated by Django 5.0.3 on 2024-05-31 14:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_vitalsigns'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vitalsigns',
            old_name='created_at',
            new_name='date',
        ),
        migrations.AlterField(
            model_name='vitalsigns',
            name='blood_pressure',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='vitalsigns',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.userprofile'),
        ),
    ]
