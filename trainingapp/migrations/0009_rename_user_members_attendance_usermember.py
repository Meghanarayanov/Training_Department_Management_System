# Generated by Django 5.0.6 on 2024-05-31 06:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trainingapp', '0008_rename_user_member_attendance_user_members'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attendance',
            old_name='user_members',
            new_name='usermember',
        ),
    ]
