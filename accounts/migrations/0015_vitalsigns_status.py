# Generated by Django 5.0.3 on 2024-06-01 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_prescription_updated_at_alter_prescription_doctor_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vitalsigns',
            name='status',
            field=models.CharField(default='Posted to Doctor', max_length=20),
        ),
    ]
