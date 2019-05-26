from django.urls import path
from . import views
from .views import (FacultiesAndInstitutesView, DepartmentsView, SpecialtiesView, EduLevelsView, EduProgramsView, CoursesView)

urlpatterns = [
    path('', views.start_redirect, name = 'facinst-start-redirect'),
    path('faculties_institutes/', FacultiesAndInstitutesView.as_view(), name = 'faculties-institutes'),
    path('faculties_institutes/delete<int:facinst_id>', FacultiesAndInstitutesView.delete_facinst, name = 'delete-facinst'),
    path('faculties_institutes/edit<int:facinst_id>', FacultiesAndInstitutesView.edit_facinst, name = 'edit-facinst'),
    path('departments/', DepartmentsView.as_view(), name = 'departments'),
    path('departments/delete<int:department_id>', DepartmentsView.delete_department, name = 'delete-department'),
    path('departments/edit<int:department_id>', DepartmentsView.edit_department, name = 'edit-department'),
    path('specialties/', SpecialtiesView.as_view(), name = 'specialties'),
    path('specialties/delete<int:specialty_id>', SpecialtiesView.delete_specialty, name = 'delete-specialty'),
    path('specialties/edit<int:specialty_id>', SpecialtiesView.edit_specialty, name = 'edit-specialty'),
    path('educational_levels/', EduLevelsView.as_view(), name = 'edu-levels'),
    path('educational_levels/delete<int:edulevel_id>', EduLevelsView.delete_edulevel, name = 'delete-edulevel'),
    path('educational_levels/edit<int:edulevel_id>', EduLevelsView.edit_edulevel, name = 'edit-edulevel'),
    path('educational_programs/', EduProgramsView.as_view(), name = 'edu-programs'),
    path('educational_programs/delete<int:eduprogram_id>', EduProgramsView.delete_eduprogram, name = 'delete-eduprogram'),
    path('educational_programs/edit<int:eduprogram_id>', EduProgramsView.edit_eduprogram, name = 'edit-eduprogram'),
    path('ajax/load-departments/', views.load_departments, name='ajax-load-departments'),               #AJAX
    path('courses/', CoursesView.as_view(), name = 'courses'),
    path('courses/delete<int:course_id>', CoursesView.delete_course, name = 'delete-courses'),
    path('courses/edit<int:course_id>', CoursesView.edit_course, name = 'edit-courses'),
    #path('', views.register, name='register'),
]
