# Generated by Django 5.0.3 on 2024-05-29 13:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_worker_biography'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='worker',
            name='full_name_slug',
        ),
    ]