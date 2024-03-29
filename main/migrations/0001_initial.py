# Generated by Django 2.2.3 on 2019-07-12 20:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batch_id', models.CharField(max_length=50)),
                ('taskers_count', models.IntegerField()),
                ('tasks_count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Tasker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tasker_id', models.IntegerField()),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Request')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.CharField(max_length=20)),
                ('due_time', models.IntegerField()),
                ('lat', models.FloatField()),
                ('assignee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Tasker')),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Request')),
            ],
        ),
    ]
