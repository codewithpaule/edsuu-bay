# Generated by Django 5.0.3 on 2024-05-31 17:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_rename_created_at_vitalsigns_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vitalsigns',
            old_name='date',
            new_name='created_at',
        ),
    ]
