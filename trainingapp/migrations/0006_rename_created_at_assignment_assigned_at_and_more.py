# Generated by Django 5.0.6 on 2024-05-30 07:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainingapp', '0005_alter_usermember_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assignment',
            old_name='created_at',
            new_name='assigned_at',
        ),
        migrations.RenameField(
            model_name='notification',
            old_name='is_read',
            new_name='read',
        ),
        migrations.AlterField(
            model_name='notification',
            name='trainer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainingapp.usermember'),
        ),
    ]
