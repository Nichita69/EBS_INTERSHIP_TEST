# Generated by Django 4.0.4 on 2022-05-19 12:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0004_rename_task_comment_task'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='status',
            new_name='is_completed',
        ),
    ]
