# Generated by Django 2.1.7 on 2019-05-18 16:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student_management', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='groups',
            old_name='star_year',
            new_name='start_year',
        ),
    ]
