# Generated by Django 3.2.16 on 2022-10-10 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_remove_myuser_is_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='is_teacher',
            field=models.BooleanField(default=False, help_text='Mark if you are a teacher'),
        ),
    ]