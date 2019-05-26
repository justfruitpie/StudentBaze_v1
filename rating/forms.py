from django import forms
from university_structure.models import (Courses, FacultiesAndInstututes, Specialties)
from marks_system.models import EducationalYears


class SclRatingParametersForm(forms.Form):

    SEMESTER_CHOICES = (
        (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'),
        (7, '7'), (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12'),
    )

    def __init__(self, *args, **kwargs):
        self.student_id = kwargs.pop('student_id', None)
        super(SclRatingParametersForm, self).__init__(*args, **kwargs)

        self.fields['course'].label = "Курс:"
        self.fields['edu_year'].label = "Учебный год:"
        self.fields['faculty_institute'].label = "Факультет (институт):"
        self.fields['specialty'].label = "Специальность:"
        self.fields['semester'].label = "Семестр:"
        self.fields['percentage'].label = "Лимит стипендиатов в процентах:"

    course = forms.ModelChoiceField(queryset = Courses.objects.all(), required=True)
    edu_year = forms.ModelChoiceField(queryset = EducationalYears.objects.all(), required=True)
    faculty_institute = forms.ModelChoiceField(queryset = FacultiesAndInstututes.objects.all(), required=True)
    specialty = forms.ModelChoiceField(queryset = Specialties.objects.all(), required=True)
    semester = forms.ChoiceField(choices = SEMESTER_CHOICES, label="", required=True)
    percentage = forms.IntegerField(min_value = 1, max_value = 100)


class ContrRatingParametersForm(forms.Form):

    SEMESTER_CHOICES = (
        (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'),
        (7, '7'), (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12'),
    )

    def __init__(self, *args, **kwargs):
        self.student_id = kwargs.pop('student_id', None)
        super(ContrRatingParametersForm, self).__init__(*args, **kwargs)

        self.fields['course'].label = "Курс:"
        self.fields['edu_year'].label = "Учебный год:"
        self.fields['faculty_institute'].label = "Факультет (институт):"
        self.fields['specialty'].label = "Специальность:"
        self.fields['semester'].label = "Семестр:"

    course = forms.ModelChoiceField(queryset = Courses.objects.all(), required=True)
    edu_year = forms.ModelChoiceField(queryset = EducationalYears.objects.all(), required=True)
    faculty_institute = forms.ModelChoiceField(queryset = FacultiesAndInstututes.objects.all(), required=True)
    specialty = forms.ModelChoiceField(queryset = Specialties.objects.all(), required=True)
    semester = forms.ChoiceField(choices = SEMESTER_CHOICES, label="", required=True)
