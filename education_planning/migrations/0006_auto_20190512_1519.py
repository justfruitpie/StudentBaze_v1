# Generated by Django 2.1.7 on 2019-05-12 12:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('education_planning', '0005_auto_20190511_2330'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassesTypes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='IndividualTasks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200)),
                ('short_name', models.CharField(max_length=5)),
            ],
            options={
                'ordering': ['full_name'],
            },
        ),
        migrations.CreateModel(
            name='SemesterControlTypes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200)),
                ('short_name', models.CharField(max_length=5)),
            ],
            options={
                'ordering': ['full_name'],
            },
        ),
        migrations.CreateModel(
            name='Subjects',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='SyllabusesPrograms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12')])),
                ('number_of_credits', models.IntegerField()),
            ],
            options={
                'ordering': ['semester'],
            },
        ),
        migrations.CreateModel(
            name='SyllabusesProgramsClassesTypes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_hours', models.IntegerField()),
                ('class_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education_planning.ClassesTypes')),
                ('syllabus_program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education_planning.SyllabusesPrograms')),
            ],
        ),
        migrations.AddField(
            model_name='syllabusesprograms',
            name='classes_types',
            field=models.ManyToManyField(through='education_planning.SyllabusesProgramsClassesTypes', to='education_planning.ClassesTypes'),
        ),
        migrations.AddField(
            model_name='syllabusesprograms',
            name='semester_control_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education_planning.SemesterControlTypes'),
        ),
        migrations.AddField(
            model_name='syllabusesprograms',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education_planning.Subjects'),
        ),
        migrations.AddField(
            model_name='syllabusesprograms',
            name='syllabus',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education_planning.Syllabuses'),
        ),
        migrations.AlterUniqueTogether(
            name='syllabusesprogramsclassestypes',
            unique_together={('syllabus_program', 'class_type')},
        ),
        migrations.AlterUniqueTogether(
            name='syllabusesprograms',
            unique_together={('syllabus', 'semester', 'subject')},
        ),
    ]