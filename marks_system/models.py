from django.db import models
from student_management.models import Students
from education_planning.models import SyllabusesPrograms
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime
from django.utils.timezone import now

# Create your models here. 2017/2018
class EducationalYears(models.Model):
    educational_year = models.CharField(max_length=9, unique=True)

    def __str__(self):
        return self.educational_year

class CurrentEducationalYear(models.Model):
    educational_year = models.ForeignKey(EducationalYears, on_delete=models.CASCADE)

class AllEctsMakrs(models.Model):
    ects_mark = models.CharField(max_length=2, unique=True)

    def __str__(self):
        return self.ects_mark

class AllNationalMarks(models.Model):
    national_mark_ukr = models.CharField(max_length=30, unique=True)
    national_mark_rus = models.CharField(max_length=20, unique=True)
    national_mark_ukr_short = models.CharField(max_length=30, unique=True)
    national_mark_rus_short = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.national_mark_ukr

class AllMarksList(models.Model):
    mark = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)], unique=True)
    national_mark = models.ForeignKey(AllNationalMarks, on_delete=models.CASCADE)
    ects_mark = models.ForeignKey(AllEctsMakrs, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.mark) + ' - ' + str(self.national_mark.national_mark_ukr) + '   (' + str(self.ects_mark) + ')'

class StudentsMarks(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    program = models.ForeignKey(SyllabusesPrograms, on_delete=models.CASCADE)
    educational_year = models.ForeignKey(EducationalYears, on_delete=models.CASCADE)
    mark = models.ForeignKey(AllMarksList, on_delete=models.CASCADE)
    date = models.DateField(default = now)
    po_hvostovke = models.BooleanField(default = False)

    class Meta:
        unique_together = [['student', 'program', 'educational_year']]

class ActivityCategories(models.Model):
    name = models.CharField(max_length=200)
    few = models.BooleanField(default = False)

    def __str__(self):
        return self.name

class ActivitiesForExtraMarks(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(ActivityCategories, on_delete=models.CASCADE)
    number_of_extra_marks = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])

    def __str__(self):
        return str(self.name) + " - (" + str(self.number_of_extra_marks) + " балла-ів)"

class StudentsExtraMarks(models.Model):

    SEMESTER_CHOICES = (
        (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'),
        (7, '7'), (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12'),
    )

    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    semester = models.IntegerField(choices=SEMESTER_CHOICES, default=1)
    educational_year = models.ForeignKey(EducationalYears, on_delete=models.CASCADE)
    activity = models.ForeignKey(ActivitiesForExtraMarks, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['student', 'semester', 'educational_year', 'activity']]
        ordering = ['semester']
