# Generated by Django 2.1.7 on 2019-05-23 01:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('marks_system', '0007_auto_20190523_0342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentsmarks',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
