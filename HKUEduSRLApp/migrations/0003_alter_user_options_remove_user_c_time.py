# Generated by Django 4.0 on 2022-01-03 07:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HKUEduSRLApp', '0002_saveoutput_save_time_alter_saveoutput_sid'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={},
        ),
        migrations.RemoveField(
            model_name='user',
            name='c_time',
        ),
    ]