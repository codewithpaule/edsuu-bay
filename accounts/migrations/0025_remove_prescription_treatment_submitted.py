# Generated by Django 5.0.3 on 2024-06-02 18:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0024_prescription_treatment_submitted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prescription',
            name='treatment_submitted',
        ),
    ]