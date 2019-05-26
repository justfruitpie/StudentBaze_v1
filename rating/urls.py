from django.urls import path
from . import views
from .views import (ScolarshopRating, ContractRating)


urlpatterns = [
    path('', views.start_redirect, name = 'rating-start-redirect'),
    path('scolarship_rating/', ScolarshopRating.choose_rating_parameters, name = 'scolarship-rating'),
    path('scolarship_rating/results_<int:course_id>_<int:edu_year_id>_<int:facinst_id>_<int:specialty_id>_<int:semester>_<int:percentage>', ScolarshopRating.rating_results, name = 'scolarship-rating-results'),
    path('scolarship_rating/results_<int:course_id>_<int:edu_year_id>_<int:facinst_id>_<int:specialty_id>_<int:semester>_<int:percentage>/print/', ScolarshopRating.rating_results, name = 'print-scolarship-rating-results'),
    path('contract_rating/', ContractRating.choose_rating_parameters, name = 'contract-rating'),
    path('contract_rating/results_<int:course_id>_<int:edu_year_id>_<int:facinst_id>_<int:specialty_id>_<int:semester>', ContractRating.rating_results, name = 'contract-rating-results'),
    path('contract_rating/results_<int:course_id>_<int:edu_year_id>_<int:facinst_id>_<int:specialty_id>_<int:semester>/print/', ContractRating.rating_results, name = 'print-contract-rating-results'),
    path('ajax/load-semesters/', views.load_semesters, name = 'ajax-load-semesters'),
    path('ajax/load-specialties/', views.load_specialties, name = 'ajax-load-specialties'),
]
