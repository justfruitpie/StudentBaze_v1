from django.urls import path
from . import views
from .views import (GroupsView, StudentsView)


urlpatterns = [
    path('', views.start_redirect, name = 'groups-start-redirect'),
    path('groups/', GroupsView.as_view(), name = 'groups'),
    path('groups/delete<int:group_id>', GroupsView.delete_group, name = 'delete-group'),
    path('groups/edit<int:group_id>', GroupsView.edit_group, name = 'edit-group'),
    path('groups/group_<int:group_id>_students/', GroupsView.group_students, name = 'group-students'),
    path('groups/group_<int:group_id>_students/edit<int:student_id>', StudentsView.edit_student_from_group, name = 'group-students-edit'),
    path('groups/group_<int:group_id>_students/delete<int:student_id>', StudentsView.delete_student_from_group, name = 'group-students-delete'),
    path('students/', StudentsView.as_view(), name = 'students'),
    path('students/delete<int:student_id>', StudentsView.delete_student, name = 'delete-student'),
    path('students/edit<int:student_id>', StudentsView.edit_student, name = 'edit-student'),
    #path('students/student_<int:student_id>_marks/', StudentsView.student_marks, name = 'student-marks'),
    #path('students/student_<int:student_id>_marks/semester_<int:semester>_report/', StudentsView.student_marks_report, name = 'student-marks-report'),
    path('academic_performance/', StudentsView.choose_stud_for_acad_perf, name = 'academic-performance'),
    path('academic_performance/student_<int:student_id>', StudentsView.student_marks, name = 'academic-performance-student'),
    path('academic_performance/student_<int:student_id>_semester_<int:semester>/report/', StudentsView.student_marks_report, name = 'academic-performance-student-report'),
    path('semester_group_report/', GroupsView.semester_group_report_parameters, name = 'semester-group-report'),
    path('semester_group_report/group_<int:group_id>_semester_<int:semester>', GroupsView.make_semester_group_report, name = 'make-semester-group-report'),
    path('semester_group_report/group_<int:group_id>_semester_<int:semester>/print/', GroupsView.make_semester_group_report, name = 'print-semester-group-report'),
    path('ajax/load-semesters/', views.ajax_load_semesters, name='ajax-load-semesters-for-semester-report'),      #AJAX
]
