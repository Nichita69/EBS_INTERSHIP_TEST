# Generated by Django 4.0.4 on 2022-05-16 15:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0003_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='Task',
            new_name='task',
        ),
    ]
