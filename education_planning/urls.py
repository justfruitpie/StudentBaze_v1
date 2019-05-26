from django.urls import path
from . import views
from .views import (SyllabusesView, SubjectsView, SemesterControlTypesView, IndividualTasksView, ClassesTypesView, SyllabusesProgramsView)


urlpatterns = [
    path('', views.start_redirect, name = 'eduplanning-start-redirect'),
    #path('ajax/search-load-syllabuses/', views.search_load_syllabuses, name='ajax-search-load-syllabuses'),
    path('syllabuses/', SyllabusesView.as_view(), name = 'syllabuses'),
    path('syllabuses/delete<int:syllabus_id>', SyllabusesView.delete_syllabus, name = 'delete-syllabus'),
    path('syllabuses/edit<int:syllabus_id>', SyllabusesView.edit_syllabus, name = 'edit-syllabus'),
    path('subjects/', SubjectsView.as_view(), name = 'subjects'),
    path('subjects/delete<int:subject_id>', SubjectsView.delete_subject, name = 'delete-subject'),
    path('subjects/edit<int:subject_id>', SubjectsView.edit_subject, name = 'edit-subject'),
    path('semester_control_types/', SemesterControlTypesView.as_view(), name = 'semester-control-types'),
    path('semester_control_types/delete<int:semester_control_type_id>', SemesterControlTypesView.delete_semester_control_type, name = 'delete-semester-control-type'),
    path('semester_control_types/edit<int:semester_control_type_id>', SemesterControlTypesView.edit_semester_control_type, name = 'edit-semester-control-type'),
    path('individual_tasks/', IndividualTasksView.as_view(), name = 'individual-tasks'),
    path('individual_tasks/delete<int:individual_task_id>', IndividualTasksView.delete_individual_task, name = 'delete-individual-task'),
    path('individual_tasks/edit<int:individual_task_id>', IndividualTasksView.edit_individual_task, name = 'edit-individual-task'),
    path('classes_types/', ClassesTypesView.as_view(), name = 'classes-types'),
    path('classes_types/delete<int:classes_type_id>', ClassesTypesView.delete_classes_type, name = 'delete-classes-type'),
    path('classes_types/edit<int:classes_type_id>', ClassesTypesView.edit_classes_type, name = 'edit-classes-type'),
    path('syllabuses/syllabus<int:syllabus_id>programs', SyllabusesProgramsView.as_view(), name = 'syllabus-programs'),
    path('syllabuses/syllabus<int:syllabus_id>programs/delete<int:syllabus_prog_id>', SyllabusesProgramsView.delete_syllabus_program, name = 'delete-syllabus-prog'),
    path('syllabuses/syllabus<int:syllabus_id>programs/edit<int:syllabus_prog_id>', SyllabusesProgramsView.edit_syllabus_program, name = 'edit-syllabus-prog'),
    path('syllabuses/syllabus<int:syllabus_id>programs/program_<int:syllabus_prog_id>_hours_<int:classes_type_id>', SyllabusesProgramsView.set_hours_for_program, name = 'syllabus-programs-hours'),
    path('syllabuses/syllabus<int:syllabus_id>programs/program_<int:syllabus_prog_id>_hours_<int:classes_type_id>_delete', SyllabusesProgramsView.delete_hours_for_program, name = 'delete-syllabus-programs-hours'),
    #path('syllabuses/programs<int:syllabus_id>', SyllabusesView.edit_syllabus, name = 'syllabus-program'), individual_tasks
    ]
