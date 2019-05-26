from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib import messages
from .models import Syllabuses
from .models import Subjects
from .models import SemesterControlTypes
from .models import IndividualTasks
from .models import ClassesTypes
from .models import SyllabusesPrograms
from .models import IndTaskSyllProg
from .models import SemControlSyllProg
from .models import SyllabusesProgramsClassesTypes
from .forms import SyllabusesCreationForm
from .forms import SubjectsCreationForm
from .forms import SemesterControlTypesCreationForm
from .forms import IndividualTasksCreationForm
from .forms import ClassesTypesCreationForm
from .forms import SyllabusesProgramsCreationForm
from .forms import SetHoursForm

# Create your views here.
def start_redirect(request):
    return HttpResponseRedirect('syllabuses/')

class SyllabusesProgramsView(View):
    form_class = SyllabusesProgramsCreationForm
    #initial = {'key': 'value'}
    template_name = 'education_planning/syllabuses_programs.html'

    def get(self, request, syllabus_id, *args, **kwargs):
        form = SyllabusesProgramsCreationForm()

        #return render(request, self.template_name, {'form': form})
        context= {'syll_progs': SyllabusesPrograms.objects.filter(syllabus_id = syllabus_id),
                    'syllabus' : Syllabuses.objects.filter(id = syllabus_id).get(),
                    'form' : form}
        return render(request, self.template_name, context)

    def post(self, request, syllabus_id, *args, **kwargs):
        form = self.form_class(request.POST, syllabus_id = syllabus_id)
        if form.is_valid():

            ########Syllabus creation######
            syllabus = Syllabuses.objects.filter(id = syllabus_id).get()
            semester = form['semester'].value()
            subject = Subjects.objects.filter(id = form['subject'].value()).get()
            #semester_control_type = SemesterControlTypes.objects.filter(id = form['semester_control_type'].value()).get()
            number_of_credits = form['number_of_credits'].value()
            current_syll_prog = SyllabusesPrograms.objects.create(syllabus = syllabus, semester = semester, subject=subject,
             number_of_credits=number_of_credits)

            #######ControlTypes creation#########
            if form['semester_control_type'].value() != "":
                semester_control_type = SemesterControlTypes.objects.filter(id = form['semester_control_type'].value()).get()
                SemControlSyllProg.objects.create(syllabus_program = current_syll_prog, semester_control_type = semester_control_type)

            #######ClassesTypes creation#########
            classes_types = form['classes_types'].value()
            for class_type_id in classes_types:
                class_type = ClassesTypes.objects.filter(id = class_type_id).get()
                SyllabusesProgramsClassesTypes.objects.create(syllabus_program = current_syll_prog, class_type = class_type)

            #######Individual creation#########
            if form['individual_task'].value() != "":
                individual_task = IndividualTasks.objects.filter(id = form['individual_task'].value()).get()
                IndTaskSyllProg.objects.create(syllabus_program = current_syll_prog, individual_task = individual_task)
            messages.add_message(request, messages.INFO, 'Дисциплина учебного плана была создана, теперь необходимо выставить часы для каждого вида занятий. ' +
            'Дициплинам с невыставленными часами соответствует оранжевая строка таблицы.')
            return HttpResponseRedirect(self.request.path_info)

        context= {'syll_progs': SyllabusesPrograms.objects.filter(syllabus_id = syllabus_id),
                    'syllabus' : Syllabuses.objects.filter(id = syllabus_id).get(),
                    'form' : form}
        return render(request, self.template_name, context)

    def edit_syllabus_program(request, syllabus_id, syllabus_prog_id):
        if(SyllabusesPrograms.objects.filter(id = syllabus_prog_id).exists()):
            instance = get_object_or_404(SyllabusesPrograms, id=syllabus_prog_id)
            form = SyllabusesProgramsCreationForm(request.POST or None, instance = instance)

            if(SemControlSyllProg.objects.filter(syllabus_program_id = syllabus_prog_id).exists()):
                form.fields['semester_control_type'].initial = SemControlSyllProg.objects.filter(syllabus_program_id = syllabus_prog_id).get().semester_control_type
            if(IndTaskSyllProg.objects.filter(syllabus_program_id = syllabus_prog_id).exists()):
                form.fields['individual_task'].initial = IndTaskSyllProg.objects.filter(syllabus_program_id = syllabus_prog_id).get().individual_task

            if form.is_valid():

                if form['semester_control_type'].value() != "":
                    semester_control_type = SemesterControlTypes.objects.filter(id = form['semester_control_type'].value()).get()
                    if(SemControlSyllProg.objects.filter(syllabus_program_id = syllabus_prog_id).exists()):
                        sem_contr_syll_prog_inst = SemControlSyllProg.objects.filter(syllabus_program_id = syllabus_prog_id).get()
                        sem_contr_syll_prog_inst.semester_control_type = semester_control_type
                        sem_contr_syll_prog_inst.save()
                    else:
                        SemControlSyllProg.objects.create(syllabus_program_id = syllabus_prog_id, semester_control_type = semester_control_type)
                else:
                    if (SemControlSyllProg.objects.filter(syllabus_program_id = syllabus_prog_id).exists()):
                        SemControlSyllProg.objects.filter(syllabus_program_id = syllabus_prog_id).delete()

                if form['individual_task'].value() != "":
                    individual_task = IndividualTasks.objects.filter(id = form['individual_task'].value()).get()
                    if(IndTaskSyllProg.objects.filter(syllabus_program_id = syllabus_prog_id).exists()):
                        ind_task_syll_prog_inst = IndTaskSyllProg.objects.filter(syllabus_program_id = syllabus_prog_id).get()
                        ind_task_syll_prog_inst.individual_task = individual_task
                        ind_task_syll_prog_inst.save()
                    else:
                        IndTaskSyllProg.objects.create(syllabus_program_id = syllabus_prog_id, individual_task = individual_task)
                else:
                    if (IndTaskSyllProg.objects.filter(syllabus_program_id = syllabus_prog_id).exists()):
                        IndTaskSyllProg.objects.filter(syllabus_program_id = syllabus_prog_id).delete()

                for j in SyllabusesProgramsClassesTypes.objects.filter(syllabus_program_id = instance.id):
                    delete = True
                    for k in form['classes_types'].value():
                        #new = True                          #Механизм удаления ненужных занятий
                        if int(k) == j.class_type_id:
                            delete = False
                    if delete:
                        j.delete()

                for k in form['classes_types'].value():
                    new = True
                    for j in SyllabusesProgramsClassesTypes.objects.filter(syllabus_program_id = instance.id):
                        if int(k) == j.class_type_id:
                            new = False                      #Механизм добавления новых занятий
                    if new:
                        tempClassType = ClassesTypes.objects.filter(id = k).get()
                        #syllabus_program = current_syll_prog, class_type = class_type
                        SyllabusesProgramsClassesTypes.objects.create(syllabus_program = instance, class_type = tempClassType)

                instance = form.save(commit=False)
                instance.save()
                return HttpResponseRedirect('/education_planning/syllabuses/syllabus' + str(syllabus_id) +'programs')

            context= {'form': form,
                      'instance': instance,}
            return render(request, 'education_planning/edit_syllabus_program.html', context)
        return HttpResponseRedirect('/education_planning/syllabuses/syllabus' + str(syllabus_id) +'programs')

    def set_hours_for_program(request, syllabus_id, syllabus_prog_id, classes_type_id):
        if(SyllabusesProgramsClassesTypes.objects.filter(class_type_id = classes_type_id, syllabus_program_id = syllabus_prog_id).exists()):
            instance = get_object_or_404(SyllabusesProgramsClassesTypes, class_type_id = classes_type_id, syllabus_program_id = syllabus_prog_id)
            form = SetHoursForm(request.POST or None, instance = instance)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                return HttpResponseRedirect('/education_planning/syllabuses/syllabus' + str(syllabus_id) + 'programs')

            context= {'form': form,
                    'instance': instance}
            return render(request, 'education_planning/set_hours_for_program.html', context)
        return HttpResponseRedirect('/education_planning/syllabuses/syllabus' + str(syllabus_id) + 'programs')

    def delete_hours_for_program(request, syllabus_id, syllabus_prog_id, classes_type_id):
        if(SyllabusesProgramsClassesTypes.objects.filter(class_type_id = classes_type_id, syllabus_program_id = syllabus_prog_id).exists()):
            SyllabusesProgramsClassesTypes.objects.filter(class_type_id = classes_type_id, syllabus_program_id = syllabus_prog_id).delete()
        return HttpResponseRedirect('/education_planning/syllabuses/syllabus' + str(syllabus_id) + 'programs')

    def delete_syllabus_program(request, syllabus_id, syllabus_prog_id):
        #syllabus_id = 0
        if(SyllabusesPrograms.objects.filter(id = syllabus_prog_id).exists()):
            #syllabus_id = SyllabusesPrograms.objects.filter(id = syllabus_prog_id).get().syllabus_id
            SyllabusesPrograms.objects.filter(id = syllabus_prog_id).delete()
        return HttpResponseRedirect('/education_planning/syllabuses/syllabus' + str(syllabus_id) + 'programs')


class SyllabusesView(View):
    form_class = SyllabusesCreationForm
    #initial = {'key': 'value'}
    template_name = 'education_planning/syllabuses.html'

    def get(self, request, *args, **kwargs):
        form = SyllabusesCreationForm()
        #return render(request, self.template_name, {'form': form})
        context= {'syllabuses': Syllabuses.objects.all(),
                    'form' : form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            #
            return HttpResponseRedirect('/education_planning/syllabuses/')

        return render(request, self.template_name, {'form': form})

    def edit_syllabus(request, syllabus_id):
        if(Syllabuses.objects.filter(id = syllabus_id).exists()):
            instance = get_object_or_404(Syllabuses, id=syllabus_id)
            form = SyllabusesCreationForm(request.POST or None, instance = instance)
            if form.is_valid():

                instance = form.save(commit=False)
                instance.save()
                return HttpResponseRedirect('/education_planning/syllabuses/')

            context= {'form': form,
                      'instance': instance,}
            return render(request, 'education_planning/edit_syllabus.html', context)
        return HttpResponseRedirect('/education_planning/syllabuses/')

    def delete_syllabus(request, syllabus_id):
        if(Syllabuses.objects.filter(id = syllabus_id).exists()):
            Syllabuses.objects.filter(id = syllabus_id).delete()
        return HttpResponseRedirect('/education_planning/syllabuses/')


class SubjectsView(View):
    form_class = SubjectsCreationForm
    #initial = {'key': 'value'}
    template_name = 'education_planning/subjects.html'

    def get(self, request, *args, **kwargs):
        form = SubjectsCreationForm()
        #return render(request, self.template_name, {'form': form})
        context= {'subjects': Subjects.objects.all(),
                    'form' : form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            #
            return HttpResponseRedirect('/education_planning/subjects/')

        return render(request, self.template_name, {'form': form})

    def edit_subject(request, subject_id):
        if(Subjects.objects.filter(id = subject_id).exists()):
            instance = get_object_or_404(Subjects, id=subject_id)
            form = SubjectsCreationForm(request.POST or None, instance = instance)
            if form.is_valid():

                instance = form.save(commit=False)
                instance.save()
                return HttpResponseRedirect('/education_planning/subjects/')

            context= {'form': form,
                      'instance': instance,}
            return render(request, 'education_planning/edit_subject.html', context)
        return HttpResponseRedirect('/education_planning/subjects/')

    def delete_subject(request, subject_id):
        if(Subjects.objects.filter(id = subject_id).exists()):
            Subjects.objects.filter(id = subject_id).delete()
        return HttpResponseRedirect('/education_planning/subjects/')


class SemesterControlTypesView(View):
    form_class = SemesterControlTypesCreationForm
    #initial = {'key': 'value'}
    template_name = 'education_planning/semester_control_types.html'

    def get(self, request, *args, **kwargs):
        form = SemesterControlTypesCreationForm()
        #return render(request, self.template_name, {'form': form})
        context= {'semester_control_types': SemesterControlTypes.objects.all(),
                    'form' : form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            #
            return HttpResponseRedirect('/education_planning/semester_control_types/')

        return render(request, self.template_name, {'form': form})

    def edit_semester_control_type(request, semester_control_type_id):
        if(SemesterControlTypes.objects.filter(id = semester_control_type_id).exists()):
            instance = get_object_or_404(SemesterControlTypes, id=semester_control_type_id)
            form = SemesterControlTypesCreationForm(request.POST or None, instance = instance)
            if form.is_valid():

                instance = form.save(commit=False)
                instance.save()
                return HttpResponseRedirect('/education_planning/semester_control_types/')

            context= {'form': form,
                      'instance': instance,}
            return render(request, 'education_planning/edit_semester_control_type.html', context)
        return HttpResponseRedirect('/education_planning/semester_control_types/')

    def delete_semester_control_type(request, semester_control_type_id):
        if(SemesterControlTypes.objects.filter(id = semester_control_type_id).exists()):
            SemesterControlTypes.objects.filter(id = semester_control_type_id).delete()
        return HttpResponseRedirect('/education_planning/semester_control_types/')


class IndividualTasksView(View):
    form_class = IndividualTasksCreationForm
    #initial = {'key': 'value'}
    template_name = 'education_planning/individual_tasks.html'

    def get(self, request, *args, **kwargs):
        form = IndividualTasksCreationForm()
        #return render(request, self.template_name, {'form': form})
        context= {'individual_tasks': IndividualTasks.objects.all(),
                    'form' : form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            #
            return HttpResponseRedirect('/education_planning/individual_tasks/')

        return render(request, self.template_name, {'form': form})

    def edit_individual_task(request, individual_task_id):
        if(IndividualTasks.objects.filter(id = individual_task_id).exists()):
            instance = get_object_or_404(IndividualTasks, id=individual_task_id)
            form = IndividualTasksCreationForm(request.POST or None, instance = instance)
            if form.is_valid():

                instance = form.save(commit=False)
                instance.save()
                return HttpResponseRedirect('/education_planning/individual_tasks/')

            context= {'form': form,
                      'instance': instance,}
            return render(request, 'education_planning/edit_individual_tasks.html', context)
        return HttpResponseRedirect('/education_planning/individual_tasks/')

    def delete_individual_task(request, individual_task_id):
        if(IndividualTasks.objects.filter(id = individual_task_id).exists()):
            IndividualTasks.objects.filter(id = individual_task_id).delete()
        return HttpResponseRedirect('/education_planning/individual_tasks/')


class ClassesTypesView(View):
    form_class = ClassesTypesCreationForm
    #initial = {'key': 'value'}
    template_name = 'education_planning/classes_types.html'

    def get(self, request, *args, **kwargs):
        form = ClassesTypesCreationForm()
        #return render(request, self.template_name, {'form': form})
        context= {'classes_types': ClassesTypes.objects.all(),
                    'form' : form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            #
            return HttpResponseRedirect('/education_planning/classes_types/')

        return render(request, self.template_name, {'form': form})

    def edit_classes_type(request, classes_type_id):
        if(ClassesTypes.objects.filter(id = classes_type_id).exists()):
            instance = get_object_or_404(ClassesTypes, id=classes_type_id)
            form = ClassesTypesCreationForm(request.POST or None, instance = instance)
            if form.is_valid():

                instance = form.save(commit=False)
                instance.save()
                return HttpResponseRedirect('/education_planning/classes_types/')

            context= {'form': form,
                      'instance': instance,}
            return render(request, 'education_planning/edit_classes_types.html', context)
        return HttpResponseRedirect('/education_planning/classes_types/')

    def delete_classes_type(request, classes_type_id):
        if(ClassesTypes.objects.filter(id = classes_type_id).exists()):
            ClassesTypes.objects.filter(id = classes_type_id).delete()
        return HttpResponseRedirect('/education_planning/classes_types/')
