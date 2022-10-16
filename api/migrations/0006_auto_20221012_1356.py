# Generated by Django 3.2.16 on 2022-10-12 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_chapter_lecture_task_lecturetext_lectureimage_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chapter',
            name='course',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='task',
        ),
        migrations.RemoveField(
            model_name='course',
            name='author',
        ),
        migrations.RemoveField(
            model_name='grade',
            name='student',
        ),
        migrations.RemoveField(
            model_name='grade',
            name='task',
        ),
        migrations.RemoveField(
            model_name='lecture',
            name='chapter',
        ),
        migrations.RemoveField(
            model_name='lecturefile',
            name='lecture',
        ),
        migrations.RemoveField(
            model_name='lectureimage',
            name='lecture',
        ),
        migrations.RemoveField(
            model_name='lecturetext',
            name='lecture',
        ),
        migrations.RemoveField(
            model_name='task',
            name='chapter',
        ),
        migrations.AddField(
            model_name='chapter',
            name='lecture',
            field=models.ManyToManyField(to='api.Lecture'),
        ),
        migrations.AddField(
            model_name='chapter',
            name='task',
            field=models.ManyToManyField(to='api.Task'),
        ),
        migrations.AddField(
            model_name='course',
            name='chapter',
            field=models.ManyToManyField(to='api.Chapter'),
        ),
        migrations.AddField(
            model_name='lecture',
            name='lecture_file',
            field=models.ManyToManyField(to='api.LectureFile'),
        ),
        migrations.AddField(
            model_name='lecture',
            name='lecture_image',
            field=models.ManyToManyField(to='api.LectureImage'),
        ),
        migrations.AddField(
            model_name='lecture',
            name='lecture_text',
            field=models.ManyToManyField(to='api.LectureText'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='average_grade',
            field=models.ManyToManyField(to='api.Grade'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='courses',
            field=models.ManyToManyField(to='api.Course'),
        ),
        migrations.AddField(
            model_name='task',
            name='comment',
            field=models.ManyToManyField(to='api.Comment'),
        ),
        migrations.AddField(
            model_name='task',
            name='grade',
            field=models.ManyToManyField(to='api.Grade'),
        ),
        migrations.AlterField(
            model_name='lecturefile',
            name='file',
            field=models.FileField(upload_to=''),
        ),
        migrations.AlterField(
            model_name='lectureimage',
            name='image',
            field=models.ImageField(upload_to=''),
        ),
    ]
