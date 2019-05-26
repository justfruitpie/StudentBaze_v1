from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='start-page'),
    #path('structure/', views.about, name='blog-about'),
]
