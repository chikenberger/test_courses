# Generated by Django 3.2.16 on 2022-10-13 13:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20221013_1248'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='author',
        ),
    ]
