# Generated by Django 2.1.7 on 2019-05-19 11:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marks_system', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='allectsmakrs',
            old_name='EctsMark',
            new_name='ects_mark',
        ),
        migrations.RenameField(
            model_name='allnationalmarks',
            old_name='national_mark_ukr_shotr',
            new_name='national_mark_ukr_short',
        ),
    ]