import math
import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.views import View
from .forms import SclRatingParametersForm
from .forms import ContrRatingParametersForm
from marks_system.models import (StudentsMarks, StudentsExtraMarks, EducationalYears)
from education_planning.models import (SyllabusesPrograms, Syllabuses)
from student_management.models import (Students, Groups)
from university_structure.models import (FacultiesAndInstututes, EducationalPrograms, FucultyInstituteSpecialty, Courses, Specialties)

# Create your views here.

def start_redirect(request):
    return HttpResponseRedirect('scolarship_rating/')

def load_semesters(request):
    course = Courses.objects.filter(id = request.GET.get('course_id')).get()
    semesters = []
    if int(course.course) == 1:
        semesters.append(1);
        semesters.append(2);
    elif int(course.course) == 2:
        semesters.append(3);
        semesters.append(4);
    elif int(course.course) == 3:
        semesters.append(5);
        semesters.append(6);
    elif int(course.course) == 4:
        semesters.append(7);
        semesters.append(8);
    elif int(course.course) == 5:
        semesters.append(7);
        semesters.append(8);
    elif int(course.course) == 6:
        semesters.append(7);
        semesters.append(8);
    return render(request, 'rating/dropdown_semesters.html', {'semesters': semesters})

def load_specialties(request):
    facinst = FacultiesAndInstututes.objects.filter(id = request.GET.get('facinst_id')).get()
    facinsts_specialties = FucultyInstituteSpecialty.objects.filter(faculty_insitute = facinst)
    list = []
    for item in facinsts_specialties:
        list.append(item.specialty_id)
    specialties = Specialties.objects.filter(id__in = list)
    return render(request, 'rating/dropdown_specialties.html', {'specialties': specialties})

class ScolarshopRating(View):

    def choose_rating_parameters(request, *args, **kwargs):
        form = SclRatingParametersForm(request.POST or None)
        if request.method == 'GET':
            form.fields['semester'].choices = SEMESTER_CHOICES = ((1, '---------'),)
            form.fields['specialty'].queryset = Specialties.objects.none()
        if form.is_valid():
            course = form['course'].value()
            edu_year = form['edu_year'].value()
            facinst = form['faculty_institute'].value()
            specialty = form['specialty'].value()
            semester = form['semester'].value()
            percentage = form['percentage'].value()
            return HttpResponseRedirect('/rating/scolarship_rating/results_' + str(course) + '_' + str(edu_year) + '_' + str(facinst)+'_' + str(specialty) + '_' +str(semester) + '_' + str(percentage))
        context= {'form' : form}
        return render(request, 'rating/scolarship_rating_parameters.html', context)

    def rating_results(request, course_id, edu_year_id, facinst_id, specialty_id, semester , percentage):
        percentage = percentage

        course = Courses.objects.filter(id = course_id).get()         #Получили курс из запроса
        edu_year = EducationalYears.objects.filter(id = edu_year_id).get()

        facinst_specs = FucultyInstituteSpecialty.objects.filter(faculty_insitute_id = facinst_id, specialty_id = specialty_id)
        eduprogs = EducationalPrograms.objects.filter(faculty_insitute_specialty__in = facinst_specs)

        ###SATRT YEAR ALGORITHM###
        course_number = course.course
        if(course_number < 5):
            group_start_year = int(str(edu_year.educational_year)[5:9]) - int(course.course)
        elif(course_number == 5):
            group_start_year = int(str(edu_year.educational_year)[5:9]) - 1
        else:
            group_start_year = int(str(edu_year.educational_year)[5:9]) - 2
        #########################

        groups = Groups.objects.filter(educational_program__in = eduprogs, start_year = group_start_year)
        students = Students.objects.filter(group__in = groups, finance_source_id = 1)       #Получили список студентов для рейтинга

        if not groups:
            messages.add_message(request, messages.ERROR, 'Удовлетворяющие заданным параметрам данные отсутствуют')
            return HttpResponseRedirect('/rating/scolarship_rating/')
        if not students:
            messages.add_message(request, messages.ERROR, 'Удовлетворяющие заданным параметрам данные отсутствуют')
            return HttpResponseRedirect('/rating/scolarship_rating/')

        ###DATA STRUCTURE FOR RATING RESULTS###
        class SubjectsAndMarksForRating():
            def __init__(self, subject, mark):
                self.subject = subject
                self.mark = mark

        class ratingData():
            def __init__(self, student, academic_mark, rating_mark, subjects_and_marks_drop_down_list, extra_marks_drop_down_list):
                self.student = student
                self.academic_mark = academic_mark
                self.rating_mark = rating_mark
                self.subjects_and_marks_drop_down_list = subjects_and_marks_drop_down_list
                self.extra_marks_drop_down_list = extra_marks_drop_down_list
        ########################################

        rating_data_list = []
        for student in students:
            student_syllabus = student.group.syllabus
            student_programs = SyllabusesPrograms.objects.filter(syllabus = student_syllabus, semester = semester)
            student_marks = StudentsMarks.objects.filter(student = student, program__in = student_programs, educational_year = edu_year)
            student_extra_marks = StudentsExtraMarks.objects.filter(student = student, semester = semester, educational_year = edu_year)

            if student_programs.count() == 0:
                messages.add_message(request, messages.ERROR, 'Удовлетворяющие заданным параметрам данные отсутствуют')
                return HttpResponseRedirect('/rating/scolarship_rating/')

            list_of_extra_marks = [ ]
            list_of_extra_marks_for_rating = [ ]
            list_of_extra_marks_without_few = [ ]
            list_of_act_categories_without_few = [ ]

            student_subjects_and_marks_list_dr_down = []
            student_extra_marks_list_dr_down = []

            for ex_mark in student_extra_marks:
                list_of_extra_marks.append(ex_mark)

            student_marks_sum = 0

            ###FOR RATING MARK###
            rating_mark = 0
            sum_of_coef_mult_mark = 0
            #####################

            addToRating = True
            for program in student_programs:
                for mark in student_marks:
                    if mark.po_hvostovke:
                        addToRating = False
                    if program.id == mark.program.id:
                        student_marks_sum = student_marks_sum + int(mark.mark.mark)
                        sum_of_coef_mult_mark = sum_of_coef_mult_mark + (int(mark.mark.mark) * int(program.number_of_credits))
                        student_subjects_and_marks_list_dr_down.append(SubjectsAndMarksForRating(program.subject, mark.mark))

            if student_programs.count() != student_marks.count():
                addToRating = False
            if addToRating:
                extra_marks_for_rating = 0

                if len(list_of_extra_marks) > 0:
                    for extra_mark in list_of_extra_marks:
                        if extra_mark.activity.category.few == False:
                            needToAdd = True
                            for act_category_without_few in list_of_act_categories_without_few:
                                if act_category_without_few == extra_mark.activity.category:
                                    needToAdd = False
                            if needToAdd:
                                list_of_act_categories_without_few.append(extra_mark.activity.category)
                            list_of_extra_marks_without_few.append(extra_mark)
                        else:
                            list_of_extra_marks_for_rating.append(extra_mark)

                #На этом этапе получаем 3 списка: list_of_extra_marks_for_rating | list_of_extra_marks_without_few | list_of_act_categories_without_few
                # list_of_act_categories_without_few - Отдельные категории, которые могут быть засчитаны единожды

                for i in list_of_act_categories_without_few:
                    extra_marks_one_category_temp_list = []
                    for j in list_of_extra_marks_without_few:
                        if (i == j.activity.category):
                            extra_marks_one_category_temp_list.append(j)
                    if len(extra_marks_one_category_temp_list) > 0:
                        max = extra_marks_one_category_temp_list[0]
                        for extra_mark_from_one_category_list in extra_marks_one_category_temp_list:
                            if extra_mark_from_one_category_list.activity.number_of_extra_marks  > max.activity.number_of_extra_marks:
                                max = extra_mark_from_one_category_list
                        list_of_extra_marks_for_rating.append(max)               #Учитываем одну максимальную из нескольких

                for extra_mark_for_rating in list_of_extra_marks_for_rating:
                    extra_marks_for_rating = int(extra_mark_for_rating.activity.number_of_extra_marks) + extra_marks_for_rating

                if extra_marks_for_rating > 10 :
                    extra_marks_for_rating = 10;

                rating_mark = (90 * sum_of_coef_mult_mark)/3000 + extra_marks_for_rating
                academic_mark = student_marks_sum / student_programs.count()

                ######################################


                ######################################


                rating_data_list.append(ratingData(student, academic_mark, rating_mark, student_subjects_and_marks_list_dr_down, list_of_extra_marks_for_rating))


        #for item in rating_data_list:
            #print(str(item.student) + " " + str(item.academic_mark) + " " + str(item.rating_mark))

        groupsString = ""
        for group in groups:
            groupsString = groupsString + group.name + ", "
        groupsString = groupsString[: -2]

        rating_data_list.sort(key = lambda x: x.rating_mark, reverse = True)

        number_of_positions = len(rating_data_list)
        number_of_scolarships = number_of_positions*percentage/100
        number_of_scolarships = math.floor(number_of_scolarships)

        context= { 'rating_data_list' : rating_data_list,
                    'course' : course,
                    'edu_year' : edu_year,
                    'faculty' : FacultiesAndInstututes.objects.filter(id = facinst_id).get(),
                    'sepecialty' : Specialties.objects.filter(id = specialty_id).get(),
                    'semester' : semester,
                    'groupsString' : groupsString,
                    'number_of_positions' : number_of_positions,
                    'number_of_scolarships' : number_of_scolarships,
                    'percentage' : percentage,
                    'current_time' : datetime.datetime.now()
                    }

        if str(request.path)[-6 :] == 'print/':
            return render(request, 'rating/print_scolarship_rating_results.html', context)
        else:
            return render(request, 'rating/scolarship_rating_results.html', context)

    def print_rating_results(request, course_id, edu_year_id, facinst_id, specialty_id, semester):
        return HttpResponseRedirect('/rating/scolarship_rating/')

class ContractRating(View):

    def choose_rating_parameters(request, *args, **kwargs):
        form = ContrRatingParametersForm(request.POST or None)
        if request.method == 'GET':
            form.fields['semester'].choices = SEMESTER_CHOICES = ((1, '---------'),)
            form.fields['specialty'].queryset = Specialties.objects.none()
        if form.is_valid():
            course = form['course'].value()
            edu_year = form['edu_year'].value()
            facinst = form['faculty_institute'].value()
            specialty = form['specialty'].value()
            semester = form['semester'].value()
            return HttpResponseRedirect('/rating/contract_rating/results_' + str(course) + '_' + str(edu_year) + '_' + str(facinst)+'_' + str(specialty) + '_' +str(semester))
        context= {'form' : form}
        return render(request, 'rating/contract_rating_parameters.html', context)

    def rating_results(request, course_id, edu_year_id, facinst_id, specialty_id, semester):
        course = Courses.objects.filter(id = course_id).get()         #Получили курс из запроса
        edu_year = EducationalYears.objects.filter(id = edu_year_id).get()

        facinst_specs = FucultyInstituteSpecialty.objects.filter(faculty_insitute_id = facinst_id, specialty_id = specialty_id)
        eduprogs = EducationalPrograms.objects.filter(faculty_insitute_specialty__in = facinst_specs)

        ###SATRT YEAR ALGORITHM###
        course_number = course.course
        if(course_number < 5):
            group_start_year = int(str(edu_year.educational_year)[5:9]) - int(course.course)
        elif(course_number == 5):
            group_start_year = int(str(edu_year.educational_year)[5:9]) - 1
        else:
            group_start_year = int(str(edu_year.educational_year)[5:9]) - 2
        #########################

        groups = Groups.objects.filter(educational_program__in = eduprogs, start_year = group_start_year)
        students = Students.objects.filter(group__in = groups, finance_source_id = 2)       #Получили список студентов для рейтинга

        if not groups:
            messages.add_message(request, messages.ERROR, 'Удовлетворяющие заданным параметрам данные отсутствуют')
            return HttpResponseRedirect('/rating/contract_rating/')
        if not students:
            messages.add_message(request, messages.ERROR, 'Удовлетворяющие заданным параметрам данные отсутствуют')
            return HttpResponseRedirect('/rating/contract_rating/')

        ###DATA STRUCTURE FOR RATING RESULTS###
        class SubjectsAndMarksForRating():
            def __init__(self, subject, mark):
                self.subject = subject
                self.mark = mark

        class ratingData():
            def __init__(self, student, academic_mark, rating_mark, subjects_and_marks_drop_down_list, extra_marks_drop_down_list):
                self.student = student
                self.academic_mark = academic_mark
                self.rating_mark = rating_mark
                self.subjects_and_marks_drop_down_list = subjects_and_marks_drop_down_list
                self.extra_marks_drop_down_list = extra_marks_drop_down_list
        ########################################

        rating_data_list = []
        for student in students:
            student_syllabus = student.group.syllabus
            student_programs = SyllabusesPrograms.objects.filter(syllabus = student_syllabus, semester = semester)
            student_marks = StudentsMarks.objects.filter(student = student, program__in = student_programs, educational_year = edu_year)
            student_extra_marks = StudentsExtraMarks.objects.filter(student = student, semester = semester, educational_year = edu_year)

            if student_programs.count() == 0:
                messages.add_message(request, messages.ERROR, 'Удовлетворяющие заданным параметрам данные отсутствуют')
                return HttpResponseRedirect('/rating/scolarship_rating/')

            list_of_extra_marks = [ ]
            list_of_extra_marks_for_rating = [ ]
            list_of_extra_marks_without_few = [ ]
            list_of_act_categories_without_few = [ ]

            student_subjects_and_marks_list_dr_down = []
            student_extra_marks_list_dr_down = []

            for ex_mark in student_extra_marks:
                list_of_extra_marks.append(ex_mark)

            student_marks_sum = 0

            ###FOR RATING MARK###
            rating_mark = 0
            sum_of_coef_mult_mark = 0
            #####################

            addToRating = True
            for program in student_programs:
                for mark in student_marks:
                    if mark.po_hvostovke:
                        addToRating = False
                    if program.id == mark.program.id:
                        student_marks_sum = student_marks_sum + int(mark.mark.mark)
                        sum_of_coef_mult_mark = sum_of_coef_mult_mark + (int(mark.mark.mark) * int(program.number_of_credits))
                        student_subjects_and_marks_list_dr_down.append(SubjectsAndMarksForRating(program.subject, mark.mark))

            if student_programs.count() != student_marks.count():
                addToRating = False
            if addToRating:
                extra_marks_for_rating = 0

                if len(list_of_extra_marks) > 0:
                    for extra_mark in list_of_extra_marks:
                        if extra_mark.activity.category.few == False:
                            needToAdd = True
                            for act_category_without_few in list_of_act_categories_without_few:
                                if act_category_without_few == extra_mark.activity.category:
                                    needToAdd = False
                            if needToAdd:
                                list_of_act_categories_without_few.append(extra_mark.activity.category)
                            list_of_extra_marks_without_few.append(extra_mark)
                        else:
                            list_of_extra_marks_for_rating.append(extra_mark)

                #На этом этапе получаем 3 списка: list_of_extra_marks_for_rating | list_of_extra_marks_without_few | list_of_act_categories_without_few
                # list_of_act_categories_without_few - Отдельные категории, которые могут быть засчитаны единожды

                for i in list_of_act_categories_without_few:
                    extra_marks_one_category_temp_list = []
                    for j in list_of_extra_marks_without_few:
                        if (i == j.activity.category):
                            extra_marks_one_category_temp_list.append(j)
                    if len(extra_marks_one_category_temp_list) > 0:
                        max = extra_marks_one_category_temp_list[0]
                        for extra_mark_from_one_category_list in extra_marks_one_category_temp_list:
                            if extra_mark_from_one_category_list.activity.number_of_extra_marks  > max.activity.number_of_extra_marks:
                                max = extra_mark_from_one_category_list
                        list_of_extra_marks_for_rating.append(max)               #Учитываем одну максимальную из нескольких

                for extra_mark_for_rating in list_of_extra_marks_for_rating:
                    extra_marks_for_rating = int(extra_mark_for_rating.activity.number_of_extra_marks) + extra_marks_for_rating

                if extra_marks_for_rating > 10 :
                    extra_marks_for_rating = 10;

                rating_mark = (90 * sum_of_coef_mult_mark)/3000 + extra_marks_for_rating
                academic_mark = student_marks_sum / student_programs.count()

                ######################################


                ######################################


                rating_data_list.append(ratingData(student, academic_mark, rating_mark, student_subjects_and_marks_list_dr_down, list_of_extra_marks_for_rating))


        #for item in rating_data_list:
            #print(str(item.student) + " " + str(item.academic_mark) + " " + str(item.rating_mark))

        groupsString = ""
        for group in groups:
            groupsString = groupsString + group.name + ", "
        groupsString = groupsString[: -2]

        rating_data_list.sort(key = lambda x: x.rating_mark, reverse = True)


        context= { 'rating_data_list' : rating_data_list,
                    'course' : course,
                    'edu_year' : edu_year,
                    'faculty' : FacultiesAndInstututes.objects.filter(id = facinst_id).get(),
                    'sepecialty' : Specialties.objects.filter(id = specialty_id).get(),
                    'semester' : semester,
                    'groupsString' : groupsString,
                    'current_time' : datetime.datetime.now()
                    }

        if str(request.path)[-6 :] == 'print/':
            return render(request, 'rating/print_contract_rating_results.html', context)
        else:
            return render(request, 'rating/contract_rating_results.html', context)

    def print_rating_results(request, course_id, edu_year_id, facinst_id, specialty_id, semester):
        return HttpResponseRedirect('/rating/scolarship_rating/')
