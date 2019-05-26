from django import forms
from django.contrib import messages
from .models import Syllabuses
from .models import Subjects
from .models import SemesterControlTypes
from .models import IndividualTasks
from .models import ClassesTypes
from .models import SyllabusesPrograms
from .models import SyllabusesProgramsClassesTypes

class SyllabusesCreationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SyllabusesCreationForm, self).__init__(*args, **kwargs)

        self.fields['cypher'].label = "Шифр:"
        self.fields['cypher'].widget.attrs['placeholder'] = "Введите шифр учебного плана"

        self.fields['educational_program'].label = "Образовательная программа:"
        self.fields['educational_program'].widget.attrs['placeholder'] = "Выберете образовательную программу"

        self.fields['year_of_approval'].label = "Год утверждения:"
        #self.fields['year_of_approval'].widget = forms.SelectDateWidget

    class Meta:
        model = Syllabuses
        fields = ['cypher', 'educational_program', 'year_of_approval']


class SubjectsCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SubjectsCreationForm, self).__init__(*args, **kwargs)

        self.fields['name'].label = "Название:"
        self.fields['name'].widget.attrs['placeholder'] = "Введите название дисциплины"

    class Meta:
        model = Subjects
        fields = ['name']

class SemesterControlTypesCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SemesterControlTypesCreationForm, self).__init__(*args, **kwargs)

        self.fields['full_name'].label = "Полное название:"
        self.fields['full_name'].widget.attrs['placeholder'] = "Введите полное название вида семестрового контроля"

        self.fields['short_name'].label = "Краткое название:"
        self.fields['short_name'].widget.attrs['placeholder'] = "Введите краткое название вида семестрового контроля"

    class Meta:
        model = SemesterControlTypes
        fields = ['full_name', 'short_name']

class IndividualTasksCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(IndividualTasksCreationForm, self).__init__(*args, **kwargs)

        self.fields['full_name'].label = "Полное название:"
        self.fields['full_name'].widget.attrs['placeholder'] = "Введите полное название индивидуального задания"

        self.fields['short_name'].label = "Краткое название:"
        self.fields['short_name'].widget.attrs['placeholder'] = "Введите краткое название индивидуального задания"

    class Meta:
        model = IndividualTasks
        fields = ['full_name', 'short_name']

class ClassesTypesCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ClassesTypesCreationForm, self).__init__(*args, **kwargs)

        self.fields['name'].label = "Название:"
        self.fields['name'].widget.attrs['placeholder'] = "Введите название типа занятий"

    class Meta:
        model = ClassesTypes
        fields = ['name']

class SyllabusesProgramsCreationForm(forms.ModelForm):
    individual_task = forms.ModelChoiceField(queryset=IndividualTasks.objects.all(), required=False)
    semester_control_type = forms.ModelChoiceField(queryset=SemesterControlTypes.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        self.syllabus_id = kwargs.pop('syllabus_id', None)
        super(SyllabusesProgramsCreationForm, self).__init__(*args, **kwargs)

        self.fields['semester'].label = "Семестр:"
        self.fields['subject'].label = "Дисциплина:"
        self.fields['semester_control_type'].label = "Вид семестрового контроля:"
        self.fields['individual_task'].label = "Индивидуальное задание:"
        self.fields['number_of_credits'].label = "Количество кредитов:"
        self.fields['classes_types'].label = "Типы занятий:"
        self.fields['classes_types'].required = False


    class Meta:
        model = SyllabusesPrograms
        fields = ["semester", "subject", "semester_control_type", "individual_task",
        "number_of_credits", "classes_types"]

    def clean_number_of_credits(self, *args, **kwargs):
        entered_number_of_credits = self.cleaned_data.get("number_of_credits")
        if entered_number_of_credits <= 0:
            raise forms.ValidationError("Количество кредитов не может равняться нулю или быть отрицательным")
        semester = self.cleaned_data.get("semester")
        syllabus_id = self.syllabus_id
        sum_of_semcredits = 0
        for i in SyllabusesPrograms.objects.filter(semester = semester, syllabus_id = syllabus_id):
            sum_of_semcredits = sum_of_semcredits + i.number_of_credits
        sum_of_semcredits = sum_of_semcredits + entered_number_of_credits
        if sum_of_semcredits > 30:
            raise forms.ValidationError("Сумма кредитов за семестр не может превышать 30. Ваша сумма кредитов: " + str(sum_of_semcredits) + ".")
        return entered_number_of_credits

class SetHoursForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SetHoursForm, self).__init__(*args, **kwargs)

        self.fields['number_of_hours'].label = "Количетсво часов:"
        self.fields['number_of_hours'].required = False

    class Meta:
        model = SyllabusesProgramsClassesTypes
        fields = ["number_of_hours"]

    def clean_number_of_hours(self, *args, **kwargs):
        number_of_hours = self.cleaned_data.get("number_of_hours")
        if number_of_hours <= 0:
            raise forms.ValidationError("Количество часов не может равняться нулю или быть отрицательным")
        syll_prog_id = self.instance.syllabus_program.id
        number_of_credits = SyllabusesPrograms.objects.get(pk = syll_prog_id).number_of_credits
        sum = 0
        for i in SyllabusesProgramsClassesTypes.objects.filter(syllabus_program_id = syll_prog_id):
            if i.number_of_hours != None:
                sum = int(i.number_of_hours) + int(sum)
        #print('sss' + str(number_of_hours))
        if number_of_hours != None:
                sum = sum + number_of_hours
        if(sum > 30 * number_of_credits):
            raise forms.ValidationError("Общее кол-во часов не может быть больше чем " + str(30 * number_of_credits) +" (кол-во кредитов * 30)" +
            ". Ваше общее кол-во часов: " + str(sum) )
        return number_of_hours
