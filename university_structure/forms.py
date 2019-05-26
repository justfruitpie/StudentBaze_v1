from django import forms
from .models import FacultiesAndInstututes
from .models import Departments
from .models import Specialties
from .models import EducationalLevels
from .models import EducationalPrograms
from .models import FucultyInstituteSpecialty
from .models import Courses

class FacInstsCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FacInstsCreationForm, self).__init__(*args, **kwargs)

        self.fields['name'].label = "Название:"
        self.fields['name'].widget.attrs['placeholder'] = "Введите название факультета или института"

        self.fields['cypher'].label = "Шифр:"
        self.fields['cypher'].widget.attrs['placeholder'] = "Введите шифр факультета или института"

        self.fields['specialty'].label = "Специальности факультета (института):"

    class Meta:
        model = FacultiesAndInstututes
        fields = ['name', 'cypher', 'specialty']

class DepartmentsCreationForm(forms.ModelForm):
    faculty_insitute = forms.ModelChoiceField(queryset=FacultiesAndInstututes.objects.all(), empty_label="")

    def __init__(self, *args, **kwargs):
        super(DepartmentsCreationForm, self).__init__(*args, **kwargs)

        self.fields['name'].label = "Название:"
        self.fields['name'].widget.attrs['placeholder'] = "Введите название кафедры"

        self.fields['cypher'].label = "Шифр:"
        self.fields['cypher'].widget.attrs['placeholder'] = "Введите шифр кафедры"

        self.fields['faculty_insitute'].label = "Выберите факультет(институт):"

    class Meta:
        model = Departments
        fields = ['name', 'cypher', 'faculty_insitute']

class SpecialtiesCreationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SpecialtiesCreationForm, self).__init__(*args, **kwargs)

        self.fields['name'].label = "Название:"
        self.fields['name'].widget.attrs['placeholder'] = "Название специальности"

        self.fields['cypher'].label = "Шифр:"
        self.fields['cypher'].widget.attrs['placeholder'] = "Введите шифр специальности"

    class Meta:
        model = Specialties
        fields = ['name', 'cypher']

class EduLevelsCreationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EduLevelsCreationForm, self).__init__(*args, **kwargs)

        self.fields['name'].label = "Название:"
        self.fields['name'].widget.attrs['placeholder'] = "Название образовательного уровня"

    class Meta:
        model = EducationalLevels
        fields = ['name']


class EduProgramsCreationForm(forms.ModelForm):
    faculty_insitute_specialty = forms.ModelChoiceField(queryset=FucultyInstituteSpecialty.objects.all(), empty_label="")
    department = forms.ModelChoiceField(queryset=Departments.objects.all(), empty_label="")
    educational_level = forms.ModelChoiceField(queryset=EducationalLevels.objects.all(), empty_label=None)

    def __init__(self, *args, **kwargs):
        super(EduProgramsCreationForm, self).__init__(*args, **kwargs)

        self.fields['name'].label = "Название:"
        self.fields['name'].widget.attrs['placeholder'] = "Введите название образовательной программы"

        self.fields['cypher'].label = "Шифр:"
        self.fields['cypher'].widget.attrs['placeholder'] = "Введите шифр образовательной программы"

        self.fields['faculty_insitute_specialty'].label = "Специальность:"

        self.fields['department'].label = "Кафедра:"
        self.fields['educational_level'].label = "Образовательный уровень:"

    class Meta:
        model = EducationalPrograms
        fields = ['name', 'cypher', 'faculty_insitute_specialty', 'department', 'educational_level']

    def clean_department(self, *args, **kwargs):
        #print(type(self.cleaned_data))
        department = self.cleaned_data.get("department")
        faculty_insitute_specialty = self.cleaned_data.get("faculty_insitute_specialty")
        if department.faculty_insitute_id == faculty_insitute_specialty.faculty_insitute_id:
            return department
        else:
            raise forms.ValidationError(str(department) + " не соответствует " +
            str(FacultiesAndInstututes.objects.filter(id = faculty_insitute_specialty.faculty_insitute_id).get()))

class CoursesDataCreationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CoursesDataCreationForm, self).__init__(*args, **kwargs)

        self.fields['course'].label = "Курс:"
        self.fields['year'].label = "Год поступления:"
        self.fields['educational_level'].label = "Образовательный уровень:"
        #self.fields['name'].widget.attrs['placeholder'] = "Введите название образовательной программы"

    class Meta:
        model = Courses
        fields = ['course', 'year', 'educational_level']
