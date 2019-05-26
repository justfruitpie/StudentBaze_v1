from django.db import models
import datetime
from university_structure.models import EducationalPrograms

# Create your models here.
class Syllabuses(models.Model):

    YEAR_CHOICES = []
    for r in range(2014, (datetime.datetime.now().year+1)):
        YEAR_CHOICES.append((r,r))

    cypher = models.CharField(max_length=50, unique=True)
    educational_program = models.ForeignKey(EducationalPrograms, on_delete=models.CASCADE)
    year_of_approval = models.IntegerField(('year'), choices=YEAR_CHOICES, default=datetime.datetime.now().year)

    def __str__(self):
        return str(self.cypher) + " - " + str(self.educational_program.name) + " (" + str(self.educational_program.cypher) + ")"

    class Meta:
         ordering = ['cypher']

class Subjects(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
         ordering = ['name']

class IndividualTasks(models.Model):
    full_name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=5)

    def getShortName(self):
        return str(self.short_name)

    def __str__(self):
        return self.full_name

    class Meta:
         ordering = ['full_name']

class SemesterControlTypes(models.Model):
    full_name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=5)

    def getShortName(self):
        return str(self.short_name)

    def __str__(self):
        return self.full_name


class ClassesTypes(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
         ordering = ['name']

class SyllabusesPrograms(models.Model):

    SEMESTER_CHOICES = (
        (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'),
        (7, '7'), (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12'),
    )

    syllabus = models.ForeignKey(Syllabuses, on_delete=models.CASCADE)
    semester = models.IntegerField(choices=SEMESTER_CHOICES, default=1)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    #semester_control_type = models.ForeignKey(SemesterControlTypes, on_delete=models.CASCADE)
    #individual_task = models.ForeignKey(IndividualTasks, on_delete=models.CASCADE)
    number_of_credits = models.IntegerField()
    classes_types = models.ManyToManyField(ClassesTypes, through='SyllabusesProgramsClassesTypes')

    def __str__(self):
        return str(self.syllabus) + " " + str(self.semester) + " " + str(self.subject)

    def getSemControl(self):
        semester_control_type = SemControlSyllProg.objects.filter(syllabus_program_id = self.id).get().semester_control_type
        return str(semester_control_type)

    def getIndTask(self):
        individual_task = IndTaskSyllProg.objects.filter(syllabus_program_id = self.id).get().individual_task
        return str(individual_task)

    def getClassesTypes(self):
        classes_types = SyllabusesProgramsClassesTypes.objects.filter(syllabus_program_id = self.id)
        return classes_types

    def checkHours(self):
        classes_types = SyllabusesProgramsClassesTypes.objects.filter(syllabus_program_id = self.id)
        for class_type in classes_types:
            if class_type.number_of_hours == None:
                return True
        return False

    def getHours(self):
        hours = SyllabusesProgramsClassesTypes.objects.filter(syllabus_program = self)
        hours_str = ""
        for item in hours:
            if item.number_of_hours == None:
                return ""
            else:
                hours_str = hours_str + (str(item.number_of_hours) + " ")
        return hours_str

    class Meta:
         unique_together = [['syllabus', 'semester', 'subject']]
         ordering = ['semester']

class SemControlSyllProg(models.Model):
    syllabus_program = models.OneToOneField(SyllabusesPrograms, on_delete=models.CASCADE)
    semester_control_type = models.ForeignKey(SemesterControlTypes, on_delete=models.CASCADE)

class IndTaskSyllProg(models.Model):
    syllabus_program = models.OneToOneField(SyllabusesPrograms, on_delete=models.CASCADE)
    individual_task = models.ForeignKey(IndividualTasks, on_delete=models.CASCADE)

class SyllabusesProgramsClassesTypes(models.Model):
    syllabus_program = models.ForeignKey(SyllabusesPrograms, on_delete=models.CASCADE)
    class_type = models.ForeignKey(ClassesTypes, on_delete=models.CASCADE)
    number_of_hours = models.IntegerField(null=True)

    def __str__(self):
        return self.name

    def getHours(self):
        if self.number_of_hours == None:
            return ""
        else:
            return ': ' + str(self.number_of_hours)

    class Meta:
         unique_together = [['syllabus_program', 'class_type']]
         #ordering = ['semester']
