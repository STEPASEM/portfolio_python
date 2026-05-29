from django.urls import path
from . import views

urlpatterns = [
    # Главная страница
    path('', views.index, name='index'),

    # Основные разделы
    path('courses/', views.courses_list, name='courses_list'),
    path('students/', views.students_list, name='students_list'),
    path('enrollments/', views.enrollments_list, name='enrollments_list'),

    # OLAP-куб
    path('olap/', views.olap_index, name='olap_index'),
    path('olap/query/', views.olap_query, name='olap_query'),
]