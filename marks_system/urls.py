from django.urls import path
from . import views
from .views import (EctsMarksView, EducationalYearsView, NationalMarksView, GeneralMarksView, SetMarksToGroupView, ActivityCategoriesView,
                        ActivitiesForExtraMarksView, SetExtraMarks)

urlpatterns = [
    path('', views.start_redirect, name = 'marks-system-start-redirect'),
    path('all_ects_marks/', EctsMarksView.as_view(), name = 'ects-marks'),
    path('all_ects_marks/delete<int:ects_mark_id>', EctsMarksView.delete_ects_mark, name = 'delete-ects-mark'),
    path('all_ects_marks/edit<int:ects_mark_id>', EctsMarksView.edit_ects_mark, name = 'edit-ects-mark'),
    path('all_national_marks/', NationalMarksView.as_view(), name = 'national-marks'),
    path('all_national_marks/delete<int:national_mark_id>', NationalMarksView.delete_national_mark, name = 'delete-national-mark'),
    path('all_national_marks/edit<int:national_mark_id>', NationalMarksView.edit_national_mark, name = 'edit-national-mark'),
    path('general_marks/', GeneralMarksView.as_view(), name = 'general-marks'),
    path('general_marks/delete<int:general_mark_id>', GeneralMarksView.delete_general_mark, name = 'delete-general-mark'),
    path('general_marks/edit<int:general_mark_id>', GeneralMarksView.edit_general_mark, name = 'edit-general-mark'),
    path('educational_years/', EducationalYearsView.as_view(), name = 'educational-years'),
    path('educational_years/delete<int:edu_year_id>', EducationalYearsView.delete_edu_year, name = 'delete-edu-year'),
    path('educational_years/edit<int:edu_year_id>', EducationalYearsView.edit_edu_year, name = 'edit-edu-year'),
    path('set_marks_to_group/', SetMarksToGroupView.group_selection, name = 'set-marks-to-group-select'),
    path('set_marks_to_group/group<int:group_id>', SetMarksToGroupView.program_selection, name = 'set-marks-to-group-select-prog'),
    path('set_marks_to_group/ajax/load-programs/', views.load_programs_ajax, name = 'load-programs-ajax'),                      #AJAX
    path('ajax/load-educational_years/', views.load_educational_years_ajax, name='load-edu-years-ajax'),
    path('ajax/load-group-semesters/', views.load_group_semesters_ajax, name='load-group-semesters-ajax'),
    path('set_marks_to_group/group<int:group_id>/year_<int:educational_year_id>_program<int:syllabus_program_id>', SetMarksToGroupView.student_selection, name = 'set-marks-to-group-select-prog'),
    path('set_marks_to_group/group<int:group_id>/year_<int:educational_year_id>_program<int:syllabus_program_id>/delete_mark_student<int:student_id>', SetMarksToGroupView.delete_mark_from_group, name = 'delete-mark-to-group-select-prog'),
    path('extra_marks/', views.extra_marks_redirect, name = 'extra-marks'),
    path('extra_marks/activity_categories/', ActivityCategoriesView.as_view(), name = 'extra-marks-activity-categories'),
    path('extra_marks/activity_categories/delete<int:activity_category_id>', ActivityCategoriesView.delete_activity_category, name = 'delete-extra-marks-activity-category'),
    path('extra_marks/activity_categories/edit<int:activity_category_id>', ActivityCategoriesView.edit_activity_category, name = 'edit-extra-marks-activity-category'),
    path('extra_marks/activities/', ActivitiesForExtraMarksView.as_view(), name = 'extra-marks-activities'),
    path('extra_marks/activities/delete<int:activity_id>', ActivitiesForExtraMarksView.delete_activity, name = 'delete-extra-marks-activities'),
    path('extra_marks/activities/edit<int:activity_id>', ActivitiesForExtraMarksView.edit_activity, name = 'edit-extra-marks-activities'),
    path('extra_marks/set_extra_marks/', SetExtraMarks.chooseStudent, name = 'extra-marks-choose-student'),
    path('extra_marks/set_extra_marks/student<int:student_id>', SetExtraMarks.student_extra_marks, name = 'extra-marks-student'),
    path('extra_marks/set_extra_marks/student<int:student_id>/delete<int:extra_mark_id>', SetExtraMarks.delete_student_extra_marks, name = 'delete-extra-marks-student'),
]

#set_marks_to_group/group1/program25/delete_mark3
