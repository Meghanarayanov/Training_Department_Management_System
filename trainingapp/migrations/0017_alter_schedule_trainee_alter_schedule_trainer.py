# Generated by Django 5.0.6 on 2024-06-03 12:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainingapp', '0016_alter_schedule_trainee_alter_schedule_trainer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='trainee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trainee_schedules', to='trainingapp.assignment'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='trainer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trainer_schedules', to='trainingapp.assignment'),
        ),
    ]
