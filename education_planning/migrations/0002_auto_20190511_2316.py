# Generated by Django 2.1.7 on 2019-05-11 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education_planning', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='syllabuses',
            name='year_of_approval',
            field=models.IntegerField(choices=[(2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019)], default=2019, max_length=4),
        ),
    ]
