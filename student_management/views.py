from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
import datetime
from django.utils.timezone import utc
from django.views import View
from education_planning.models import Syllabuses
from .models import Groups
from .models import Students
from education_planning.models import (SyllabusesPrograms, SemControlSyllProg)
from marks_system.models import StudentsMarks
from .forms import GroupsCreationForm
from .forms import StudentsCreationForm
from .forms import SelectSemester
from .forms import SemesterGroupReportForm

# Create your views here.
def start_redirect(request):
    return HttpResponseRedirect('/student_management/groups/')

def ajax_load_semesters(request):
    group_id = request.GET.get('group_id')
    group = Groups.objects.filter(id = group_id).get()
    semesters = []
    print("HERE")
    if group.educational_program.educational_level.id == 5:
        for i in range(1, 9):
            semesters.append(i)
    elif group.educational_program.educational_level.id == 5:
        for i in range(9, 13):
            semesters.append(i)

    return render(request, 'student_management/dropdown_semesters.html', {'semesters': semesters})

class GroupsView(View):
    form_class = GroupsCreationForm
    template_name = 'student_management/groups.html'

    def get(self, request, *args, **kwargs):
        form = GroupsCreationForm()

        #return render(request, self.template_name, {'form': form})
        context= {'groups': Groups.objects.all(),
                    'form' : form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            name = form['name'].value()
            start_year = form['start_year'].value()
            syllabus = Syllabuses.objects.filter(id = form['syllabus'].value()).get()
            educational_program = syllabus.educational_program
            department = educational_program.department
            Groups.objects.create(name = name, start_year = start_year, educational_program = educational_program, syllabus = syllabus,
            department = department)
            #form.save()
            return HttpResponseRedirect('/student_management/groups/')

        return render(request, self.template_name, {'form': form})

    def edit_group(request, group_id):
        if (Groups.objects.filter(id = group_id).exists()):
            instance = get_object_or_404(Groups, id=group_id)
            form = GroupsCreationForm(request.POST or None, instance = instance)
            if form.is_valid():
                name = form['name'].value()
                start_year = form['start_year'].value()
                syllabus = Syllabuses.objects.filter(id = form['syllabus'].value()).get()
                educational_program = syllabus.educational_program
                department = educational_program.department

                instance.name = name
                instance.start_year = start_year
                instance.syllabus = syllabus
                instance.educational_program = educational_program
                instance.department = department
                instance.save()
                return HttpResponseRedirect('/student_management/groups/')

            context= {'form': form,
                      'instance': instance,}
            return render(request, 'student_management/edit_group.html', context)
        return HttpResponseRedirect('/student_management/groups/')

    def delete_group(request, group_id):
        if (Groups.objects.filter(id = group_id).exists()):
            Groups.objects.filter(id = group_id).delete()
        return HttpResponseRedirect('/student_management/groups/')

    def group_students(request, group_id):
        template = 'student_management/group_students.html'
        context= {'students': Students.objects.filter(group_id = group_id),
                    'group' : Groups.objects.filter(id = group_id).get(),}
        return render(request, template, context)

    def semester_group_report_parameters(request):
        form = SemesterGroupReportForm(request.POST or None)

        if request.method == 'GET':
            form.fields['semester'].choices = SEMESTER_CHOICES = ((1, '---------'),)

        if form.is_valid():
            semester = form['semester'].value()
            group_id = form['group'].value()
            return HttpResponseRedirect('/student_management/semester_group_report/group_' + str(group_id) + '_semester_' + str(semester))

        context= {'form' : form}
        return render(request, 'student_management/semester_group_report_param.html', context)

    def make_semester_group_report(request, group_id, semester):
        group = Groups.objects.filter(id = group_id).get()
        students = Students.objects.filter(group_id = group_id)
        syllabus_id = group.syllabus.id
        programs = SyllabusesPrograms.objects.filter(syllabus_id = syllabus_id, semester = semester)

        class SemGrRepData():
            def __init__(self, student, marks):
                self.student = student
                self.marks = marks

        listOfDataItems = []
        listOfSubjects = []
        listOfMarks = []
        zadolzhenost_count = 0
        students_with_zadolzhenosti = 0

        for student in students:
            student_marks_dict = { }
            student_marks = StudentsMarks.objects.filter(student_id = student.id, program__in = programs)
            for program in programs:
                show = True
                for mark in student_marks:
                    if program.id == mark.program.id:
                        if mark.po_hvostovke:
                            student_marks_dict[str(program.subject.name)] = 0
                            zadolzhenost_count = zadolzhenost_count + 1
                        else:
                            student_marks_dict[str(program.subject.name)] = int(mark.mark.mark)
                        show = False
                if show:
                    student_marks_dict[str(program.subject.name)] = 0
                    zadolzhenost_count = zadolzhenost_count + 1
            sorted_student_marks = sorted(student_marks_dict.items(), key = lambda x: x[0])
            listOfSubjects = []
            listOfMarks = []
            zadolzhenost = False
            for item in sorted_student_marks:
                if item[1] == 0:
                    zadolzhenost = True
                listOfSubjects.append(item[0])
                listOfMarks.append(item[1])
            if zadolzhenost:
                students_with_zadolzhenosti = students_with_zadolzhenosti + 1

            listOfDataItems.append(SemGrRepData(student, listOfMarks))

        if semester == 1 or semester == 2:
            edu_year = str(group.start_year) + '/' + str(group.start_year + 1)
        elif semester == 3 or semester == 4:
            edu_year = str(group.start_year + 1) + '/' + str(group.start_year + 2)
        elif semester == 5 or semester == 6:
            edu_year = str(group.start_year + 2) + '/' + str(group.start_year + 3)
        elif semester == 7 or semester == 8:
            edu_year = str(group.start_year + 3) + '/' + str(group.start_year + 4)
        if semester == 9 or semester == 10:
            edu_year = str(group.start_year) + '/' + str(group.start_year + 1)
        if semester == 11 or semester == 12:
            edu_year = str(group.start_year + 1) + '/' + str(group.start_year + 2)


        context= {'listOfDataItems' : listOfDataItems,
                    'group' : group,
                    'semester' : semester,
                    'list_of_subjects' : listOfSubjects,
                    'zadolzhenost_count' : zadolzhenost_count,
                    'students_with_zadolzhenosti' : students_with_zadolzhenosti,
                    'edu_year' : edu_year,
                    'current_time' : datetime.datetime.now()}

        if str(request.path)[-6 :] == 'print/':
            return render(request, 'student_management/print_semester_group_report_results.html', context)
        else:
            return render(request, 'student_management/semester_group_report_results.html', context)

class StudentsView(View):
    form_class = StudentsCreationForm
    template_name = 'student_management/students.html'

    def get(self, request, *args, **kwargs):
        form = StudentsCreationForm()

        #return render(request, self.template_name, {'form': form})
        context= {'students': Students.objects.all(),
                    'form' : form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            form.save()
            return HttpResponseRedirect('/student_management/students/')

        context= {'students': Students.objects.all(),
                    'form' : form}

        return render(request, self.template_name, context)

    def edit_student(request, student_id):
        if(Students.objects.filter(id = student_id).exists()):
            instance = get_object_or_404(Students, id=student_id)
            form = StudentsCreationForm(request.POST or None, instance = instance)
            #date = str(form['date_of_birdth'].value())[8:10] + "/" + str(form['date_of_birdth'].value())[5:7] + "/" + str(form['date_of_birdth'].value())[0:4]
            #form.fields['date_of_birdth'] = date
            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                return HttpResponseRedirect('/student_management/students/')

            context= {'form': form,
                      'instance': instance,}
            return render(request, 'student_management/edit_student.html', context)
        return HttpResponseRedirect('/student_management/students/')

    def edit_student_from_group(request, group_id, student_id):
        if(Students.objects.filter(id = student_id).exists()):
            instance = get_object_or_404(Students, id=student_id)
            form = StudentsCreationForm(request.POST or None, instance = instance)
            #date = str(form['date_of_birdth'].value())[8:10] + "/" + str(form['date_of_birdth'].value())[5:7] + "/" + str(form['date_of_birdth'].value())[0:4]
            #form.fields['date_of_birdth'] = date
            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                return HttpResponseRedirect('/student_management/groups/group_' + str(group_id) + '_students/')

            context= {'form': form,
                      'instance': instance,
                      'group' : Groups.objects.filter(id = group_id).get(),}
            return render(request, 'student_management/edit_student_from_group.html', context)
        return HttpResponseRedirect('/student_management/groups/group_' + str(group_id) + '_students/')

    def delete_student(request, student_id):
        if (Students.objects.filter(id = student_id).exists()):
            Students.objects.filter(id = student_id).delete()
        return HttpResponseRedirect('/student_management/students/')

    def delete_student_from_group(request, group_id, student_id):
        if (Students.objects.filter(id = student_id).exists()):
            Students.objects.filter(id = student_id).delete()
        return HttpResponseRedirect('/student_management/groups/group_' + str(group_id) + '_students/')

    def choose_stud_for_acad_perf(request):
        context= {'students': Students.objects.all()}
        return render(request, 'student_management/choose_stud_for_acad_perf.html', context)

    def student_marks(request, student_id):
        form = SelectSemester(request.POST or None)
        if form.is_valid():
            semester = form['semester'].value()
            return HttpResponseRedirect('/student_management/academic_performance/student_' + str(student_id) + '_semester_' + str(semester) + '/report/')

        student_marks = StudentsMarks.objects.filter(student_id = student_id)
        sum = 0
        count = 0
        for mark in student_marks:
            sum = sum + mark.mark.mark
            count = count + 1
        if count > 0:
            sum = sum/count
        context= {'student_marks': student_marks,
                    'number_of_marks' : student_marks.count(),
                    'student' : Students.objects.filter(id = student_id).get(),
                    'avarage_mark' : str(sum)[0:5],
                    'form' : form}
        return render(request, 'student_management/student_marks.html', context)

    def student_marks_report(request, student_id, semester):
        syllabus_id = Students.objects.filter(id = student_id).get().group.syllabus.id
        programs = SyllabusesPrograms.objects.filter(syllabus_id = syllabus_id, semester = semester)
        student_marks = StudentsMarks.objects.filter(student_id = student_id, program__in = programs)
        dict = {}

        class reprotData():
            def __init__(self, subject, credits, national_mark, mark, ects_mark, control_type, po_hvostovke):
                self.subject = subject
                self.credits = credits
                self.national_mark = national_mark
                self.mark = mark
                self.ects_mark = ects_mark
                self.control_type = control_type
                self.po_hvostovke = po_hvostovke

        reportDataList = []
        for prog in programs:
            show = True
            for mark in student_marks:
                if prog.id == mark.program.id:
                    reportDataList.append(reprotData(prog.subject, prog.number_of_credits, mark.mark.national_mark, mark.mark.mark, mark.mark.ects_mark, SemControlSyllProg.objects.filter(syllabus_program_id = prog.id).get().semester_control_type, po_hvostovke = mark.po_hvostovke))
                    #dict[str(prog.subject)] = mark.mark.id
                    #print (str(prog.subject) + ' : ' + str(mark.mark.mark))
                    show = False
            if show:
                reportDataList.append(reprotData(prog.subject, prog.number_of_credits, None, None, None, SemControlSyllProg.objects.filter(syllabus_program_id = prog.id).get().semester_control_type, po_hvostovke = mark.po_hvostovke))
                #dict[str(prog.subject)] = ""
                #print(str(prog.subject) + ' : -----------')
        context= {'reportData': reportDataList,
                    'student' : Students.objects.filter(id = student_id).get(),
                    'edu_program' : Students.objects.filter(id = student_id).get().group.educational_program,
                    'semester' : semester,
                    'student_marks' : student_marks,
                    'current_time' : datetime.datetime.now()
                    }
        return render(request, 'student_management/student_marks_report.html', context)
