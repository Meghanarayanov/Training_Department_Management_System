# Generated by Django 5.0.6 on 2024-06-01 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainingapp', '0009_rename_user_members_attendance_usermember'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaverequest',
            name='status',
            field=models.CharField(default='Pending', max_length=20),
        ),
    ]
