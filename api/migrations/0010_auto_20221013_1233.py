# Generated by Django 3.2.16 on 2022-10-13 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20221013_1228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapter',
            name='lecture',
            field=models.ManyToManyField(blank=True, to='api.Lecture'),
        ),
        migrations.AlterField(
            model_name='chapter',
            name='task',
            field=models.ManyToManyField(blank=True, to='api.Task'),
        ),
        migrations.AlterField(
            model_name='course',
            name='chapter',
            field=models.ManyToManyField(blank=True, to='api.Chapter'),
        ),
        migrations.AlterField(
            model_name='grade',
            name='task',
            field=models.ManyToManyField(blank=True, to='api.Task'),
        ),
        migrations.AlterField(
            model_name='lecture',
            name='lecture_file',
            field=models.ManyToManyField(blank=True, to='api.LectureFile'),
        ),
        migrations.AlterField(
            model_name='lecture',
            name='lecture_image',
            field=models.ManyToManyField(blank=True, to='api.LectureImage'),
        ),
        migrations.AlterField(
            model_name='lecture',
            name='lecture_text',
            field=models.ManyToManyField(blank=True, to='api.LectureText'),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='courses',
            field=models.ManyToManyField(blank=True, to='api.Course'),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='grades',
            field=models.ManyToManyField(blank=True, to='api.Grade'),
        ),
        migrations.AlterField(
            model_name='task',
            name='comment',
            field=models.ManyToManyField(blank=True, to='api.Comment'),
        ),
    ]