# Generated by Django 5.0.3 on 2024-06-03 01:07

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0028_remove_medicalhistory_test_medicalhistory_diagnosis_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicalhistory',
            name='doctor',
            field=models.CharField(max_length=100, verbose_name=accounts.models.UserProfile),
        ),
    ]
