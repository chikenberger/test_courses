# Generated by Django 3.2.16 on 2022-10-13 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20221013_1207'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='students',
        ),
        migrations.AddField(
            model_name='myuser',
            name='courses',
            field=models.ManyToManyField(to='api.Course'),
        ),
    ]
