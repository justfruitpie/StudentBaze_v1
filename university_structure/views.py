from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib import messages
from .models import FacultiesAndInstututes
from .models import Departments
from .models import Specialties
from .models import FucultyInstituteSpecialty
from .models import EducationalLevels
from .models import EducationalPrograms
from .models import Courses
from .forms import FacInstsCreationForm
from .forms import DepartmentsCreationForm
from .forms import SpecialtiesCreationForm
from .forms import EduLevelsCreationForm
from .forms import EduProgramsCreationForm
from .forms import CoursesDataCreationForm

from django import forms
from django.contrib import messages

import json
from django.http import JsonResponse

# Create your views here.
def start_redirect(request):
    return HttpResponseRedirect('faculties_institutes/')

class FacultiesAndInstitutesView(View):
    form_class = FacInstsCreationForm
    #initial = {'key': 'value'}
    template_name = 'university_structure/faculties_institutes.html'

    def get(self, request, *args, **kwargs):
        form = FacInstsCreationForm()
        #return render(request, self.template_name, {'form': form})
        context= {'facinsts': FacultiesAndInstututes.objects.all(),
                    'form' : form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            newFacInst = FacultiesAndInstututes.objects.create(cypher = form['cypher'].value(), name = form['name'].value())
            for i in form['specialty'].value():
                tempSpec = Specialties.objects.filter(id = i).get()
                FucultyInstituteSpecialty.objects.create(faculty_insitute = newFacInst, specialty = tempSpec)
            messages.add_message(request, messages.INFO, str(form['name'].value()) + ' (' + str(form['cypher'].value()) + ') создан.')
            return HttpResponseRedirect('/university_structure')

        return render(request, self.template_name, {'form': form})

    def edit_facinst(request, facinst_id):
        if(FacultiesAndInstututes.objects.filter(id = facinst_id).exists()):
            instance = get_object_or_404(FacultiesAndInstututes, id=facinst_id)
            form = FacInstsCreationForm(request.POST or None, instance = instance)
            if form.is_valid():

                for j in FucultyInstituteSpecialty.objects.filter(faculty_insitute_id = instance.id):
                    delete = True
                    for k in form['specialty'].value():
                        new = True                          #Механизм удаления ненужных
                        if int(k) == j.specialty_id:
                            delete = False
                    if delete:
                        j.delete()

                for k in form['specialty'].value():
                    new = True
                    for j in FucultyInstituteSpecialty.objects.filter(faculty_insitute_id = instance.id):
                        if int(k) == j.specialty_id:
                            new = False                      #Механизм добавления новых
                    if new:
                        tempSpec = Specialties.objects.filter(id = k).get()
                        FucultyInstituteSpecialty.objects.create(faculty_insitute = instance, specialty = tempSpec)

                faculty_insitute = FacultiesAndInstututes.objects.filter(id = facinst_id).get()
                messages.add_message(request, messages.INFO, str(faculty_insitute.name) + ' (' + str(faculty_insitute.cypher) + ') изменен.')
                instance = form.save(commit=False)
                instance.save()
                return HttpResponseRedirect('/university_structure/faculties_institutes/')

            context= {'form': form,
                      'instance': instance,}
            return render(request, 'university_structure/edit_faculties_institutes.html', context)
        return HttpResponseRedirect('/university_structure/faculties_institutes/')

    def delete_facinst(request, facinst_id):
        if(FacultiesAndInstututes.objects.filter(id = facinst_id).exists()):
            faculty_insitute = FacultiesAndInstututes.objects.filter(id = facinst_id).get()
            messages.add_message(request, messages.INFO, str(faculty_insitute.name) + ' (' + str(faculty_insitute.cypher) + ') удален.')
            FacultiesAndInstututes.objects.filter(id = facinst_id).delete()
        return HttpResponseRedirect('/university_structure')


class DepartmentsView(View):
    form_class = DepartmentsCreationForm
    initial = {'key': 'value'}
    template_name = 'university_structure/departments.html'

    def get(self, request, *args, **kwargs):
        form = DepartmentsCreationForm()
        #return render(request, self.template_name, {'form': form})
        context= {'departments': Departments.objects.all(),
                    'form' : form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            form.save()
            return HttpResponseRedirect('/university_structure/departments/')

        return render(request, self.template_name, {'form': form})

    def edit_department(request, department_id):
        if(Departments.objects.filter(id = department_id).exists()):
            instance = get_object_or_404(Departments, id=department_id)
            form = DepartmentsCreationForm(request.POST or None, instance = instance)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                return HttpResponseRedirect('/university_structure/departments/')

            context= {'form': form,
                      'instance': instance,}
            return render(request, 'university_structure/edit_departments.html', context)
        return HttpResponseRedirect('/university_structure/departments/')

    def delete_department(request, department_id):
        if(Departments.objects.filter(id = department_id).exists()):
            Departments.objects.filter(id = department_id).delete()
        return HttpResponseRedirect('/university_structure/departments/')


class SpecialtiesView(View):
    form_class = SpecialtiesCreationForm
    initial = {'key': 'value'}
    template_name = 'university_structure/specialties.html'

    def get(self, request, *args, **kwargs):
        form = SpecialtiesCreationForm()
        #return render(request, self.template_name, {'form': form})
        context= {'specialties': Specialties.objects.all(),
                    'form' : form,}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            form.save()
            return HttpResponseRedirect('/university_structure/specialties/')

        return render(request, self.template_name, {'form': form})

    def edit_specialty(request, specialty_id):
        if(Specialties.objects.filter(id = specialty_id).exists()):
            instance = get_object_or_404(Specialties, id=specialty_id)
            form = SpecialtiesCreationForm(request.POST or None, instance = instance)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                return HttpResponseRedirect('/university_structure/specialties/')

            context= {'form': form,
                      'instance': instance,}
            return render(request, 'university_structure/edit_specialty.html', context)
        return HttpResponseRedirect('/university_structure/specialties/')

    def delete_specialty(request, specialty_id):
        if(Specialties.objects.filter(id = specialty_id).exists()):
            Specialties.objects.filter(id = specialty_id).delete()
        return HttpResponseRedirect('/university_structure/specialties/')


class EduLevelsView(View):
    form_class = EduLevelsCreationForm
    initial = {'key': 'value'}
    template_name = 'university_structure/edu_levels.html'

    def get(self, request, *args, **kwargs):
        form = EduLevelsCreationForm()
        #return render(request, self.template_name, {'form': form})
        context= {'edu_levels': EducationalLevels.objects.all(),
                    'form' : form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            form.save()
            return HttpResponseRedirect('/university_structure/educational_levels/')

        context= {'edu_levels': EducationalLevels.objects.all(),
                    'form' : form}

        return render(request, self.template_name, context)

    def edit_edulevel(request, edulevel_id):
        if(EducationalLevels.objects.filter(id = edulevel_id).exists()):
            instance = get_object_or_404(EducationalLevels, id=edulevel_id)
            form = EduLevelsCreationForm(request.POST or None, instance = instance)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                return HttpResponseRedirect('/university_structure/educational_levels/')

            context= {'form': form,
                      'instance': instance,}
            return render(request, 'university_structure/edit_edulevel.html', context)
        return HttpResponseRedirect('/university_structure/educational_levels/')

    def delete_edulevel(request, edulevel_id):
        if(EducationalLevels.objects.filter(id = edulevel_id).exists()):
            EducationalLevels.objects.filter(id = edulevel_id).delete()
        return HttpResponseRedirect('/university_structure/educational_levels/')

class EduProgramsView(View):
    form_class = EduProgramsCreationForm
    initial = {'key': 'value'}
    template_name = 'university_structure/edu_programs.html'

    def get(self, request, *args, **kwargs):
        form = EduProgramsCreationForm()
        #form.fields['department'].queryset = Departments.objects.filter(id=10000)
        form.fields['department'].queryset = Departments.objects.none()
        #return render(request, self.template_name, {'form': form})
        context= {'edu_programs': EducationalPrograms.objects.all(),
                    'form' : form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            form.save()
            return HttpResponseRedirect('/university_structure/educational_programs/')

        context= {'edu_programs': EducationalPrograms.objects.all(),
                    'form' : form}
        return render(request, self.template_name, context)

    def edit_eduprogram(request, eduprogram_id):
        if(EducationalPrograms.objects.filter(id = eduprogram_id).exists()):
            instance = get_object_or_404(EducationalPrograms, id=eduprogram_id)
            form = EduProgramsCreationForm(request.POST or None, instance = instance)
            form.fields['department'].queryset = Departments.objects.filter(faculty_insitute_id = instance.faculty_insitute_specialty.faculty_insitute_id)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                return HttpResponseRedirect('/university_structure/educational_programs/')

            context= {'form': form,
                      'instance': instance,}
            return render(request, 'university_structure/edit_eduprogram.html', context)
        return HttpResponseRedirect('/university_structure/educational_programs/')

    def delete_eduprogram(request, eduprogram_id):
        if(EducationalPrograms.objects.filter(id = eduprogram_id).exists()):
            EducationalPrograms.objects.filter(id = eduprogram_id).delete()
        return HttpResponseRedirect('/university_structure/educational_programs/')

def load_departments(request):
    facinstspec_id = request.GET.get('facinstspec_id')
    #print(facinstspec_id)
    facinstspec = FucultyInstituteSpecialty.objects.filter(id = facinstspec_id)
    departments = Departments.objects.filter(faculty_insitute = facinstspec.get().faculty_insitute)
    return render(request, 'university_structure/dropdown_departments.html', {'departments': departments})


class CoursesView(View):
    form_class = CoursesDataCreationForm
    #initial = {'key': 'value'}
    template_name = 'university_structure/courses.html'

    def get(self, request, *args, **kwargs):
        form = CoursesDataCreationForm()
        #return render(request, self.template_name, {'form': form})
        context= {'courses': Courses.objects.all(),
                    'form' : form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/university_structure/courses/')

        context= {'courses': Courses.objects.all(),
                    'form' : form}
        return render(request, self.template_name, context)

    def delete_course(request, course_id):
        if(Courses.objects.filter(id = course_id).exists()):
            Courses.objects.filter(id = course_id).delete()
        return HttpResponseRedirect('/university_structure/courses/')

    def edit_course(request, course_id):
        if(Courses.objects.filter(id = course_id).exists()):
            instance = get_object_or_404(Courses, id=course_id)
            form = CoursesDataCreationForm(request.POST or None, instance = instance)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                return HttpResponseRedirect('/university_structure/courses/')

            context= {'form': form,
                      'instance': instance,}
            return render(request, 'university_structure/edit_course.html', context)
        return HttpResponseRedirect('/university_structure/courses/')
