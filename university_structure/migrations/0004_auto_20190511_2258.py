# Generated by Django 2.1.7 on 2019-05-11 19:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('university_structure', '0003_auto_20190510_1944'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='departments',
            options={'ordering': ['cypher']},
        ),
        migrations.AlterModelOptions(
            name='educationalprograms',
            options={'ordering': ['cypher']},
        ),
        migrations.AlterModelOptions(
            name='facultiesandinstututes',
            options={'ordering': ['cypher']},
        ),
        migrations.AlterModelOptions(
            name='specialties',
            options={'ordering': ['cypher']},
        ),
    ]
