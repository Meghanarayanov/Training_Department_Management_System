# Generated by Django 5.0.6 on 2024-06-01 17:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trainingapp', '0013_alter_assignment_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usermember',
            name='status',
        ),
    ]
