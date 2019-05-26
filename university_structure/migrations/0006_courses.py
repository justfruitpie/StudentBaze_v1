# Generated by Django 2.1.7 on 2019-05-23 01:19

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('university_structure', '0005_auto_20190511_2333'),
    ]

    operations = [
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.IntegerField(unique=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(6)])),
                ('year', models.IntegerField(choices=[(2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019)], default=2019, verbose_name='year')),
                ('educational_level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='university_structure.EducationalLevels')),
            ],
        ),
    ]