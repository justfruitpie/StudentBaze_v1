from django import forms
from .models import (AllEctsMakrs, EducationalYears, AllNationalMarks, AllMarksList, StudentsMarks, ActivityCategories, ActivitiesForExtraMarks,
                        StudentsExtraMarks)
from student_management.models import (Groups, Students)
from education_planning.models import SyllabusesPrograms
from django.utils import timezone


class EctsMarkCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EctsMarkCreationForm, self).__init__(*args, **kwargs)

        self.fields['ects_mark'].label = "Оценка ECTS:"
        self.fields['ects_mark'].widget.attrs['placeholder'] = "Введите оценку ECTS"

    class Meta:
        model = AllEctsMakrs
        fields = ['ects_mark']


class EducationalYearCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EducationalYearCreationForm, self).__init__(*args, **kwargs)

        self.fields['educational_year'].label = "Учебный год:"
        self.fields['educational_year'].widget.attrs['placeholder'] = "Введите учебный год в формате \"год/год\""

    class Meta:
        model = EducationalYears
        fields = ['educational_year']


class NationalMarkCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NationalMarkCreationForm, self).__init__(*args, **kwargs)

        self.fields['national_mark_ukr'].label = "Нац. оценка на украинском:"
        self.fields['national_mark_ukr'].widget.attrs['placeholder'] = "Введите нац. оценку на украинском"
        self.fields['national_mark_rus'].label = "Нац. оценка на руссокм:"
        self.fields['national_mark_rus'].widget.attrs['placeholder'] = "Введите нац. оценку на русском"
        self.fields['national_mark_ukr_short'].label = "Нац. оценка на украинском кратко:"
        self.fields['national_mark_ukr_short'].widget.attrs['placeholder'] = "Введите нац. оценку на украинском в краткой форме"
        self.fields['national_mark_rus_short'].label = "Нац. оценка на русском кратко:"
        self.fields['national_mark_rus_short'].widget.attrs['placeholder'] = "Введите нац. оценку на русском в краткой форме"

    class Meta:
        model = AllNationalMarks
        fields = ['national_mark_ukr' , 'national_mark_rus', 'national_mark_ukr_short', 'national_mark_rus_short']

class GeneralMarkCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(GeneralMarkCreationForm, self).__init__(*args, **kwargs)

        self.fields['mark'].label = "Количество баллов:"
        self.fields['mark'].widget.attrs['placeholder'] = "Введите количество баллов (от 1 до 100)"
        self.fields['national_mark'].label = "Национальная оценка:"
        self.fields['ects_mark'].label = "Оценка ECTS:"

    class Meta:
        model = AllMarksList
        fields = ['mark' , 'national_mark', 'ects_mark']


class SemesterProgramSelectionForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.group_id = kwargs.pop('group_id', None)
        super(SemesterProgramSelectionForm, self).__init__(*args, **kwargs)

        self.fields['semester'].label = "Семестр:"
        self.fields['syllabus_program'].label = "Дисциплина учебного плана:"
        self.fields['educational_year'].label = "Учебный год:"

    SEMESTER_CHOICES = (
        (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'),
        (7, '7'), (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12'),
    )

    semester = forms.ChoiceField(choices = SEMESTER_CHOICES, label="", required=True)
    syllabus_program = forms.ModelChoiceField(queryset=SyllabusesPrograms.objects.all(), required=True)
    educational_year = forms.ModelChoiceField(queryset=EducationalYears.objects.all(), required=True)

    def clean_educational_year(self, *args, **kwargs):
        group_start_year = Groups.objects.filter(id = self.group_id).get().start_year
        selected_year = self.cleaned_data.get("educational_year").educational_year
        if (Groups.objects.filter(id = self.group_id).get().educational_program.educational_level.id == 5):
            if (int(str(selected_year)[0:4]) < int(group_start_year) or int(str(selected_year)[0:4]) > (int(group_start_year)+3)):
                raise forms.ValidationError("Неверно указанный учебный год. В выбранном учебном году данная группа еще или уже не учится.")
            else:
                return self.cleaned_data.get("educational_year")
        if (Groups.objects.filter(id = self.group_id).get().educational_program.educational_level.id == 6):
            if (int(str(selected_year)[0:4]) < int(group_start_year) or int(str(selected_year)[0:4]) > (int(group_start_year)+1)):
                raise forms.ValidationError("Неверно указанный учебный год. В выбранном учебном году данная группа еще или уже не учится.")
            else:
                return self.cleaned_data.get("educational_year")


class SetStudentMarkForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(format = '%d/%m/%Y'),
                                 input_formats=('%d/%m/%Y',), initial = timezone.now())

    def __init__(self, *args, **kwargs):
        super(SetStudentMarkForm, self).__init__(*args, **kwargs)

        self.fields['mark'].label = "Оценка:"
        self.fields['po_hvostovke'].label = "По хвостовке"

    class Meta:
        model = StudentsMarks
        fields = ['mark' , 'date' ,'po_hvostovke']

class ActivityCategoriesCreationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ActivityCategoriesCreationForm, self).__init__(*args, **kwargs)

        self.fields['name'].label = "Название категории:"
        self.fields['name'].widget.attrs['placeholder'] = "Введите название категории деятельностей"
        self.fields['few'].label = "Считается несколько позиций:"

    class Meta:
        model = ActivityCategories
        fields = ['name' , 'few']

class ActivitiesForExtraMarksCreationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ActivitiesForExtraMarksCreationForm, self).__init__(*args, **kwargs)

        self.fields['name'].label = "Название достижения или вида деятельностей студента:"
        self.fields['name'].widget.attrs['placeholder'] = "Введите название достижения или вида деятельностей студента"
        self.fields['category'].label = "Категория:"
        self.fields['number_of_extra_marks'].label = "Количество баллов:"
        self.fields['number_of_extra_marks'].widget.attrs['placeholder'] = "Введите количество баллов"

    class Meta:
        model = ActivitiesForExtraMarks
        fields = ['name' , 'category', 'number_of_extra_marks']

class SetStudentExtraMarksForm(forms.Form):

    SEMESTER_CHOICES = (
        (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'),
        (7, '7'), (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12'),
    )

    activity = forms.ModelChoiceField(queryset = ActivitiesForExtraMarks.objects.all(), required=True)
    semester = forms.ChoiceField(choices = SEMESTER_CHOICES, label="", initial=1, required=True)
    educational_year = forms.ModelChoiceField(queryset = EducationalYears.objects.all(), required=True)

    def __init__(self, *args, **kwargs):
        self.student_id = kwargs.pop('student_id', None)
        super(SetStudentExtraMarksForm, self).__init__(*args, **kwargs)

        self.fields['activity'].label = "Деятельность или достижение:"
        self.fields['semester'].label = "Семестр:"
        self.fields['educational_year'].label = "Учебный год:"

    def clean_educational_year(self, *args, **kwargs):
        group = Students.objects.filter(id = self.student_id).get().group
        group_start_year = group.start_year
        selected_year = self.cleaned_data.get("educational_year").educational_year
        selected_semester = self.cleaned_data.get("semester")
        if (group.educational_program.educational_level.id == 5):
            if (int(str(selected_year)[0:4]) < int(group_start_year) or int(str(selected_year)[0:4]) > (int(group_start_year)+3)):
                raise forms.ValidationError("Неверно указанный учебный год. В выбранном учебном году данная группа еще или уже не учится.")
            else:
                if int(selected_semester) == 1 and int(str(selected_year)[0:4]) == int(group_start_year):
                    return self.cleaned_data.get("educational_year")
                elif int(selected_semester) == 2 and int(str(selected_year)[0:4]) == int(group_start_year):
                    return self.cleaned_data.get("educational_year")
                elif int(selected_semester) == 3 and int(str(selected_year)[0:4]) == (int(group_start_year)+1):
                    return self.cleaned_data.get("educational_year")
                elif int(selected_semester) == 4 and int(str(selected_year)[0:4]) == (int(group_start_year)+1):
                    return self.cleaned_data.get("educational_year")
                elif int(selected_semester) == 5 and int(str(selected_year)[0:4]) == (int(group_start_year)+2):
                    return self.cleaned_data.get("educational_year")
                elif int(selected_semester) == 6 and int(str(selected_year)[0:4]) == (int(group_start_year)+2):
                    return self.cleaned_data.get("educational_year")
                elif int(selected_semester) == 7 and int(str(selected_year)[0:4]) == (int(group_start_year)+3):
                    return self.cleaned_data.get("educational_year")
                elif int(selected_semester) == 8 and int(str(selected_year)[0:4]) == (int(group_start_year)+3):
                    return self.cleaned_data.get("educational_year")
                else:
                    raise forms.ValidationError("Учебный год не соответствует семестру")
        if (Groups.objects.filter(id = self.group_id).get().educational_program.educational_level.id == 6):
            if (int(str(selected_year)[0:4]) < int(group_start_year) or int(str(selected_year)[0:4]) > (int(group_start_year)+1)):
                raise forms.ValidationError("Неверно указанный учебный год. В выбранном учебном году данная группа еще или уже не учится.")
            else:
                if int(selected_semester) == 9 and int(str(selected_year)[0:4]) == int(group_start_year):
                    return self.cleaned_data.get("educational_year")
                elif int(selected_semester) == 10 and int(str(selected_year)[0:4]) == int(group_start_year):
                    return self.cleaned_data.get("educational_year")
                elif int(selected_semester) == 11 and int(str(selected_year)[0:4]) == (int(group_start_year)+1):
                    return self.cleaned_data.get("educational_year")
                elif int(selected_semester) == 12 and int(str(selected_year)[0:4]) == (int(group_start_year)+1):
                    return self.cleaned_data.get("educational_year")
                else:
                    raise forms.ValidationError("Учебный год не соответствует семестру")
