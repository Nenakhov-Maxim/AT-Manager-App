# Generated by Django 4.2.15 on 2024-10-21 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0012_alter_tasks_task_profile_length'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasks',
            name='worker_accepted_task',
            field=models.TextField(blank=True, verbose_name='ФИО рабочего'),
        ),
    ]
