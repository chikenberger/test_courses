# Generated by Django 4.0.6 on 2022-10-11 15:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_myuser_is_teacher'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Task',
        ),
    ]
