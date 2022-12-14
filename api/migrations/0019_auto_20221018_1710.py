# Generated by Django 3.2.16 on 2022-10-18 17:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_rename_course_author_comment_is_course_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='grade',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='grades', to='api.course'),
        ),
        migrations.CreateModel(
            name='TaskSolution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='')),
                ('student', models.EmailField(max_length=254, null=True)),
                ('grade', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.grade')),
                ('task', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='solutions', to='api.task')),
            ],
        ),
    ]
