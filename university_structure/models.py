from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime

# Create your models here.
class Specialties(models.Model):
    cypher = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return str(self.cypher) + " - " + str(self.name)

    class Meta:
         ordering = ['cypher']

class FacultiesAndInstututes(models.Model):
    cypher = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=200)
    specialty = models.ManyToManyField(Specialties, through='FucultyInstituteSpecialty')

    def __str__(self):
        return self.name

    def getSpecialties(self):
        query_res = FucultyInstituteSpecialty.objects.filter(faculty_insitute_id = self.id)
        return query_res

    class Meta:
         ordering = ['cypher']

class FucultyInstituteSpecialty(models.Model):
    faculty_insitute = models.ForeignKey(FacultiesAndInstututes, on_delete=models.CASCADE)
    specialty = models.ForeignKey(Specialties, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['faculty_insitute', 'specialty']]

    def getFacInst(self):
        return str(self.faculty_insitute)

    def getSpecialty(self):
        return str(self.specialty)

    def __str__(self):
        return str(self.specialty) + " | " + str(self.faculty_insitute) + " (" + str(self.faculty_insitute.cypher) + ")"

class Departments(models.Model):
    cypher = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=200)
    faculty_insitute = models.ForeignKey(FacultiesAndInstututes, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.cypher) + " - " + str(self.name)

    class Meta:
         ordering = ['cypher']

class EducationalLevels(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class EducationalPrograms(models.Model):
    cypher = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    faculty_insitute_specialty = models.ForeignKey(FucultyInstituteSpecialty, on_delete=models.CASCADE)
    department = models.ForeignKey(Departments, on_delete=models.CASCADE)
    educational_level = models.ForeignKey(EducationalLevels, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.cypher) + " - " + str(self.name)

    class Meta:
         ordering = ['cypher']

class Courses(models.Model):

    YEAR_CHOICES = []
    for r in range(2014, (datetime.datetime.now().year+1)):
        YEAR_CHOICES.append((r,r))

    course = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(6)], unique=True)
    year = models.IntegerField(('year'), choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    educational_level = models.ForeignKey(EducationalLevels, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.course) + ' курс - ' + str(self.educational_level.name)

    class Meta:
         ordering = ['course']
