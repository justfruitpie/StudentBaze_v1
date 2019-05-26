from django import forms
from crispy_forms.helper import FormHelper
from .models import Groups
from .models import Students
from education_planning.models import SyllabusesPrograms

class GroupsCreationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(GroupsCreationForm, self).__init__(*args, **kwargs)

        self.fields['name'].label = "Название группы:"
        self.fields['start_year'].label = "Год старта обучения:"
        self.fields['syllabus'].label = "Учебный план:"

    class Meta:
        model = Groups
        fields = ['name', 'start_year', 'syllabus']

class StudentsCreationForm(forms.ModelForm):
    date_of_birdth = forms.DateField(widget=forms.DateInput(format = '%d/%m/%Y'),
                           input_formats=('%d/%m/%Y',))

    def __init__(self, *args, **kwargs):
        super(StudentsCreationForm, self).__init__(*args, **kwargs)

        self.fields['last_name'].label = "Фамилия:"
        self.fields['first_name'].label = "Имя:"
        self.fields['middle_name'].label = "Отчество:"
        self.fields['middle_name'].required = False
        self.fields['sex'].label = "Пол:"
        self.fields['sex'].empty_label = None
        self.fields['date_of_birdth'].label = "Дата рождения:"
        self.fields['date_of_birdth'].required = False
        self.fields['date_of_birdth'].widget.attrs['placeholder'] = "Введите дату рождения в формате \"день/месяц/год\""
        self.fields['group'].label = "Академическая группа:"
        self.fields['finance_source'].label = "Источник финансирования:"
        self.fields['finance_source'].empty_label = None

    class Meta:
        model = Students
        fields = ['last_name', 'first_name', 'middle_name', 'sex', 'date_of_birdth', 'group', 'finance_source']

class SelectSemester(forms.Form):

    def __init__(self, *args, **kwargs):
        super(SelectSemester, self).__init__(*args, **kwargs)

        self.fields['semester'].label = ""

    SEMESTER_CHOICES = (
        (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'),
        (7, '7'), (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12'),
    )

    semester = forms.ChoiceField(choices = SEMESTER_CHOICES, label="", initial=1, required=True)


class SemesterGroupReportForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(SemesterGroupReportForm, self).__init__(*args, **kwargs)

        self.fields['group'].label = "Группа"
        self.fields['semester'].label = "Семестр"

    SEMESTER_CHOICES = (
        (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'),
        (7, '7'), (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12'),
    )

    group = forms.ModelChoiceField(queryset=Groups.objects.all(), empty_label="")
    semester = forms.ChoiceField(choices = SEMESTER_CHOICES, label="", initial=1, required=True)

    def clean_group(self, *args, **kwargs):
        group = self.cleaned_data.get("group")
        semester = self['semester'].value()
        students = Students.objects.filter(group_id = group.id)
        syllabus_id = group.syllabus.id
        programs = SyllabusesPrograms.objects.filter(syllabus_id = syllabus_id, semester = semester)

        print("ID: " + str(syllabus_id))
        print("SEMESTER: " + str(semester))
        if programs.count() == 0:
            raise forms.ValidationError("Выбранная группа не имеет дисциплин в своем учебном плане (возможно, для указанного семестра)")
        elif students.count() == 0:
            raise forms.ValidationError("В выбранной группе отсутствуют студенты")
        else:
            return group
