from django.apps import apps
from django.db import models
import datetime
from university_structure.models import (EducationalPrograms, Departments)
from education_planning.models import Syllabuses

# Create your models here.
class Groups(models.Model):
    YEAR_CHOICES = []
    for r in range(2014, (datetime.datetime.now().year+1)):
        YEAR_CHOICES.append((r,r))

    name = models.CharField(max_length=100)
    start_year = models.IntegerField(('year'), choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    educational_program = models.ForeignKey(EducationalPrograms, on_delete=models.CASCADE)
    syllabus = models.ForeignKey(Syllabuses, on_delete=models.CASCADE)
    department = models.ForeignKey(Departments, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name) + " (" + str(self.start_year) + ")"

class FinanceSources(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Sex(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=1, default='h')

    def __str__(self):
        return self.name

class Students(models.Model):
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100)
    sex = models.ForeignKey(Sex, on_delete=models.SET_NULL, null=True)
    date_of_birdth = models.DateField(null=True)
    group = models.ForeignKey(Groups, on_delete=models.CASCADE)
    finance_source = models.ForeignKey(FinanceSources, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.last_name) + str(self.first_name) + str(self.middle_name)

    def getWithInitials(self):
        return str(self.last_name) + " " + str(self.first_name)[0 : 1] + ". " + str(self.middle_name)[0 : 1] + "."

    def getExtraMarks(self):
        extra_marks_model = apps.get_model('marks_system.StudentsExtraMarks')
        query = extra_marks_model.objects.filter(student_id = self.id)
        if query.count() > 0:
            return query
        return None

class GroupHistory(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    start_date = models.DateField()
    group = models.ForeignKey(Groups, on_delete=models.CASCADE)
    comment = models.CharField(max_length=100)

    class Meta:
        unique_together = [['student', 'start_date']]

class FinanceHistory(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    start_date = models.DateField()
    finance_source = models.ForeignKey(FinanceSources, on_delete=models.CASCADE)
    comment = models.CharField(max_length=100)

    class Meta:
        unique_together = [['student', 'start_date']]
