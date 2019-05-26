from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib import messages
from .models import AllEctsMakrs
from .models import EducationalYears
from .models import AllNationalMarks
from .models import AllMarksList
from .models import StudentsMarks
from .models import CurrentEducationalYear
from .models import ActivityCategories
from .models import ActivitiesForExtraMarks
from .models import StudentsExtraMarks
from student_management.models import (Groups, Students)
from education_planning.models import SyllabusesPrograms
from .forms import EctsMarkCreationForm
from .forms import EducationalYearCreationForm
from .forms import NationalMarkCreationForm
from .forms import GeneralMarkCreationForm
from .forms import SemesterProgramSelectionForm
from .forms import SetStudentMarkForm
from .forms import ActivityCategoriesCreationForm
from .forms import ActivitiesForExtraMarksCreationForm
from .forms import SetStudentExtraMarksForm

CURRENT_EDU_YEAR = CurrentEducationalYear.objects.all()[:1].get().educational_year

# Create your views here.
def start_redirect(request):
    return HttpResponseRedirect('set_marks_to_group/')

def extra_marks_redirect(request):
    return HttpResponseRedirect('extra_marks/activity_categories/')

def load_group_semesters_ajax(request):
    group_id = request.GET.get('group_id')
    group = Groups.objects.filter(id = group_id).get()
    semesters = []
    if group.educational_program.educational_level.id == 5:
        for i in range(1, 9):
            semesters.append(i)
    elif group.educational_program.educational_level.id == 5:
        for i in range(9, 13):
            semesters.append(i)

    return render(request, 'mark_system/dropdown_semesters.html', {'semesters': semesters})

class EctsMarksView(View):
    form_class = EctsMarkCreationForm
    template_name = 'mark_system/ects_marks.html'

    def get(self, request, *args, **kwargs):
        form = EctsMarkCreationForm()

        context= {'ects_marks': AllEctsMakrs.objects.all(),
                    'form' : form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            #
            return HttpResponseRedirect('/marks_system/all_ects_marks/')

        return render(request, self.template_name, {'form': form})

    def edit_ects_mark(request, ects_mark_id):
        if(AllEctsMakrs.objects.filter(id = ects_mark_id).exists()):
            instance = get_object_or_404(AllEctsMakrs, id=ects_mark_id)
            form = EctsMarkCreationForm(request.POST or None, instance = instance)
            if form.is_valid():

                instance = form.save(commit=False)
                instance.save()
                return HttpResponseRedirect('/marks_system/all_ects_marks/')

            context= {'form': form,
                      'instance': instance,}
            return render(request, 'mark_system/edit_ects_mark.html', context)
        return HttpResponseRedirect('/marks_system/all_ects_marks/')

    def delete_ects_mark(request, ects_mark_id):
        if(AllEctsMakrs.objects.filter(id = ects_mark_id).exists()):
            AllEctsMakrs.objects.filter(id = ects_mark_id).delete()
        return HttpResponseRedirect('/marks_system/all_ects_marks/')


class EducationalYearsView(View):
    form_class = EducationalYearCreationForm
    template_name = 'mark_system/educational_years.html'

    def get(self, request, *args, **kwargs):
        form = EducationalYearCreationForm()

        context= {'edu_years': EducationalYears.objects.all(),
                    'form' : form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            #
            return HttpResponseRedirect('/marks_system/educational_years/')

        return render(request, self.template_name, {'form': form})

    def edit_edu_year(request, edu_year_id):
        if(EducationalYears.objects.filter(id = edu_year_id).exists()):
            instance = get_object_or_404(EducationalYears, id=edu_year_id)
            form = EducationalYearCreationForm(request.POST or None, instance = instance)
            if form.is_valid():

                instance = form.save(commit=False)
                instance.save()
                return HttpResponseRedirect('/marks_system/educational_years/')

            context= {'form': form,
                      'instance': instance,}
            return render(request, 'mark_system/edit_educational_year.html', context)
        return HttpResponseRedirect('/marks_system/educational_years/')

    def delete_edu_year(request, edu_year_id):
        if(EducationalYears.objects.filter(id = edu_year_id).exists()):
            EducationalYears.objects.filter(id = edu_year_id).delete()
        return HttpResponseRedirect('/marks_system/educational_years/')


class NationalMarksView(View):
    form_class = NationalMarkCreationForm
    template_name = 'mark_system/national_marks.html'

    def get(self, request, *args, **kwargs):
        form = NationalMarkCreationForm()

        context= {'national_marks': AllNationalMarks.objects.all(),
                    'form' : form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            #
            return HttpResponseRedirect('/marks_system/all_national_marks/')

        return render(request, self.template_name, {'form': form})

    def edit_national_mark(request, national_mark_id):
        if(AllNationalMarks.objects.filter(id = national_mark_id).exists()):
            instance = get_object_or_404(AllNationalMarks, id=national_mark_id)
            form = NationalMarkCreationForm(request.POST or None, instance = instance)
            if form.is_valid():

                instance = form.save(commit=False)
                instance.save()
                return HttpResponseRedirect('/marks_system/all_national_marks/')

            context= {'form': form,
                      'instance': instance,}
            return render(request, 'mark_system/edit_national_mark.html', context)
        return HttpResponseRedirect('/marks_system/all_national_marks/')

    def delete_national_mark(request, national_mark_id):
        if(AllNationalMarks.objects.filter(id = national_mark_id).exists()):
            AllNationalMarks.objects.filter(id = national_mark_id).delete()
        return HttpResponseRedirect('/marks_system/all_national_marks/')


class GeneralMarksView(View):
    form_class = GeneralMarkCreationForm
    template_name = 'mark_system/general_marks.html'

    def get(self, request, *args, **kwargs):
        form = GeneralMarkCreationForm()

        context= {'general_marks': AllMarksList.objects.all(),
                    'form' : form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            #
            return HttpResponseRedirect('/marks_system/general_marks/')

        context= {'general_marks': AllMarksList.objects.all(),
                    'form' : form}
        return render(request, self.template_name, context)

    def edit_general_mark(request, general_mark_id):
        if(AllMarksList.objects.filter(id = general_mark_id).exists()):
            instance = get_object_or_404(AllMarksList, id=general_mark_id)
            form = GeneralMarkCreationForm(request.POST or None, instance = instance)
            if form.is_valid():

                instance = form.save(commit=False)
                instance.save()
                return HttpResponseRedirect('/marks_system/general_marks/')

            context= {'form': form,
                      'instance': instance,}
            return render(request, 'mark_system/edit_general_mark.html', context)
        return HttpResponseRedirect('/marks_system/general_marks/')

    def delete_general_mark(request, general_mark_id):
        if(AllMarksList.objects.filter(id = general_mark_id).exists()):
            AllMarksList.objects.filter(id = general_mark_id).delete()
        return HttpResponseRedirect('/marks_system/general_marks/')


class SetMarksToGroupView(View):

    def group_selection(request, *args, **kwargs):
        context= {'groups': Groups.objects.all()}
        return render(request, 'mark_system/select_group_for_marks.html', context)

    def program_selection(request, group_id, *args, **kwargs):
        form = SemesterProgramSelectionForm(request.POST or None, group_id = group_id)

        if (request.method == 'GET'):
            print('Ne zahodit')
            form.fields['educational_year'].choices = SEMESTER_CHOICES = ((1, '---------'),)

        if (request.method == "POST"):
            if form.is_valid():
                syllabus_program_id = form['syllabus_program'].value()
                educational_year_id = form['educational_year'].value()
                return HttpResponseRedirect('/marks_system/set_marks_to_group/group' + str(group_id) + '/year_' + str(educational_year_id) + '_program' + str(syllabus_program_id))

        syllabus_id = Groups.objects.filter(id = group_id).get().syllabus_id
        form.fields['syllabus_program'].queryset = SyllabusesPrograms.objects.none()
        context= {'group': Groups.objects.filter(id = group_id).get(),
                    'group_id' : group_id,
                    'form' : form}
        return render(request, 'mark_system/select_program_for_marks.html', context)

    def student_selection(request, group_id, educational_year_id, syllabus_program_id, *args, **kwargs):
        form = SetStudentMarkForm(request.POST or None)

        if (request.method == "POST"):
            if form.is_valid():
                students = Students.objects.filter(group_id = group_id)
                for student in students:
                    if ("buttonStudent" + str(student.id)) in request.POST:
                        po_hvostovke = form['po_hvostovke'].value()
                        mark_id = form['mark'].value()
                        educational_year_id = educational_year_id
                        program_id = syllabus_program_id
                        student_id = student.id
                        if StudentsMarks.objects.filter(educational_year_id = educational_year_id, program_id = program_id, student_id = student_id).exists():
                            messages.add_message(request, messages.WARNING, 'Невозможно добавить оценку туда где она уже стоит. Удалите ее и попробуйте снова')
                            return HttpResponseRedirect('/marks_system/set_marks_to_group/group' + str(group_id) + '/year_' + str(educational_year_id) + '_program' + str(syllabus_program_id))
                        else:
                            StudentsMarks.objects.create(po_hvostovke = po_hvostovke, mark_id = mark_id, educational_year_id = educational_year_id, program_id = program_id, student_id = student_id)
                return HttpResponseRedirect('/marks_system/set_marks_to_group/group' + str(group_id) + '/year_' + str(educational_year_id) + '_program' + str(syllabus_program_id))

        context= {'students': Students.objects.filter(group_id = group_id),
                    'group' : Groups.objects.filter(id = group_id).get(),
                    'syllabus_program' : SyllabusesPrograms.objects.filter(id = syllabus_program_id).get(),
                    'marks' : StudentsMarks.objects.filter(educational_year_id = educational_year_id, program_id = syllabus_program_id),
                    'year' : EducationalYears.objects.filter(id = educational_year_id).get(),
                    'form' : form}
        return render(request, 'mark_system/select_student_for_marks.html', context)

    def delete_mark_from_group(request, group_id, syllabus_program_id, educational_year_id, student_id, *args, **kwargs):
        if(StudentsMarks.objects.filter(student_id = student_id, program_id = syllabus_program_id, educational_year_id = educational_year_id).exists()):
            StudentsMarks.objects.filter(student_id = student_id, program_id = syllabus_program_id, educational_year_id = educational_year_id).delete()
        return HttpResponseRedirect('/marks_system/set_marks_to_group/group' + str(group_id) + '/year_' + str(educational_year_id) + '_program' + str(syllabus_program_id))


def load_programs_ajax(request):
    programs = SyllabusesPrograms.objects.filter(syllabus_id = request.GET.get('syllabus_id'), semester = request.GET.get('semester'))
    return render(request, 'mark_system/dropdown_programs.html', {'programs': programs})

def load_educational_years_ajax(request):
    semester = request.GET.get('semester')
    group = Groups.objects.filter(id = request.GET.get('group_id')).get()

    if int(semester) == 1 or int(semester) == 2:
        for item in EducationalYears.objects.all():
            if int(str(item.educational_year)[0:4]) == int(group.start_year):
                return render(request, 'mark_system/dropdown_edu_years.html', {'educational_year': item})
    if int(semester) == 3 or int(semester) == 4:
        for item in EducationalYears.objects.all():
            if int(str(item.educational_year)[0:4]) == (int(group.start_year) + 1):
                return render(request, 'mark_system/dropdown_edu_years.html', {'educational_year': item})
    if int(semester) == 5 or int(semester) == 6:
        for item in EducationalYears.objects.all():
            if int(str(item.educational_year)[0:4]) == (int(group.start_year) + 2):
                return render(request, 'mark_system/dropdown_edu_years.html', {'educational_year': item})
    if int(semester) == 7 or int(semester) == 8:
        for item in EducationalYears.objects.all():
            if int(str(item.educational_year)[0:4]) == (int(group.start_year) + 3):
                return render(request, 'mark_system/dropdown_edu_years.html', {'educational_year': item})
    if int(semester) == 9 or int(semester) == 10:
        if group.educational_program.educational_level.id == 6:
            for item in EducationalYears.objects.all():
                if int(str(item.educational_year)[0:4]) == int(group.start_year):
                    return render(request, 'mark_system/dropdown_edu_years.html', {'educational_year': item})
    if int(semester) == 11 or int(semester) == 2:
        if group.educational_program.educational_level.id == 6:
            for item in EducationalYears.objects.all():
                if int(str(item.educational_year)[0:4]) == (int(group.start_year) + 1):
                    return render(request, 'mark_system/dropdown_edu_years.html', {'educational_year': item})

    return render(request, 'mark_system/dropdown_edu_years.html', {'educational_year': EducationalYears.objects.none()})

class ActivityCategoriesView(View):
    form_class = ActivityCategoriesCreationForm
    template_name = 'mark_system/activity_categories.html'

    def get(self, request, *args, **kwargs):
        form = ActivityCategoriesCreationForm()

        context= {'activity_categories': ActivityCategories.objects.all(),
                    'form' : form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            #
            return HttpResponseRedirect('/marks_system/extra_marks/activity_categories')

    def edit_activity_category(request, activity_category_id):
        if(ActivityCategories.objects.filter(id = activity_category_id).exists()):
            instance = get_object_or_404(ActivityCategories, id=activity_category_id)
            form = ActivityCategoriesCreationForm(request.POST or None, instance = instance)
            if form.is_valid():

                instance = form.save(commit=False)
                instance.save()
                return HttpResponseRedirect('/marks_system/extra_marks/activity_categories')

            context= {'form': form,
                      'instance': instance,}
            return render(request, 'mark_system/edit_activity_category.html', context)
        return HttpResponseRedirect('/marks_system/extra_marks/activity_categories')

    def delete_activity_category(request, activity_category_id):
        if(ActivityCategories.objects.filter(id = activity_category_id).exists()):
            ActivityCategories.objects.filter(id = activity_category_id).delete()
        return HttpResponseRedirect('/marks_system/extra_marks/activity_categories')


class ActivitiesForExtraMarksView(View):
    form_class = ActivitiesForExtraMarksCreationForm
    template_name = 'mark_system/activities_for_extra_marks.html'

    def get(self, request, *args, **kwargs):
        form = ActivitiesForExtraMarksCreationForm()

        context= {'activities_for_extra_marks': ActivitiesForExtraMarks.objects.all(),
                    'form' : form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            #
            return HttpResponseRedirect('/marks_system/extra_marks/activities')

    def edit_activity(request, activity_id):
        if(ActivitiesForExtraMarks.objects.filter(id = activity_id).exists()):
            instance = get_object_or_404(ActivitiesForExtraMarks, id=activity_id)
            form = ActivitiesForExtraMarksCreationForm(request.POST or None, instance = instance)
            if form.is_valid():

                instance = form.save(commit=False)
                instance.save()
                return HttpResponseRedirect('/marks_system/extra_marks/activities')

            context= {'form': form,
                      'instance': instance,}
            return render(request, 'mark_system/edit_activityy.html', context)
        return HttpResponseRedirect('/marks_system/extra_marks/activities')

    def delete_activity(request, activity_id):
        if(ActivitiesForExtraMarks.objects.filter(id = activity_id).exists()):
            ActivitiesForExtraMarks.objects.filter(id = activity_id).delete()
        return HttpResponseRedirect('/marks_system/extra_marks/activities')

class SetExtraMarks(View):

    def chooseStudent(request):
        context= {'students': Students.objects.all(),
                    }
        return render(request, 'mark_system/select_student_for_extra_marks.html', context)

    def student_extra_marks(request, student_id,  *args, **kwargs):
        form = SetStudentExtraMarksForm(request.POST or None, student_id = student_id)

        if form.is_valid():

            student = Students.objects.filter(id = student_id).get()
            activity = ActivitiesForExtraMarks.objects.filter(id = form["activity"].value()).get()
            semester = form["semester"].value()
            educational_year = EducationalYears.objects.filter(id = form["educational_year"].value()).get()
            StudentsExtraMarks.objects.create(student = student, semester = semester, educational_year = educational_year, activity = activity)
            return HttpResponseRedirect('/marks_system/extra_marks/set_extra_marks/student' + str(student_id))

        context= {'student_extra_marks': StudentsExtraMarks.objects.filter(student_id = student_id),
                    'student' : Students.objects.filter(id = student_id).get(),
                    'form' : form
                    }
        return render(request, 'mark_system/set_student_extra_marks.html', context)

    def delete_student_extra_marks(request, student_id, extra_mark_id):
        if(StudentsExtraMarks.objects.filter(id = extra_mark_id).exists()):
            StudentsExtraMarks.objects.filter(id = extra_mark_id).delete()
        return HttpResponseRedirect('/marks_system/extra_marks/set_extra_marks/student' + str(student_id))
