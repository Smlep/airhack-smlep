# Generated by Django 2.2.3 on 2019-07-12 21:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20190712_2100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='assignee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Tasker'),
        ),
        migrations.AlterField(
            model_name='tasker',
            name='tasker_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
