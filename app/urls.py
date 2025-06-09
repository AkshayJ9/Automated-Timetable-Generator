from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('',views.index,name='index'),
    path('log_in',views.log_in,name='log_in'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('show_time_table/',views.show_time_table,name='show_time_table'),
    path('create_table/',views.create_table,name='create_table'),
    path('view_time_table/',views.view_time_table,name='view_time_table'),
    path("view_teacher_schedule/",views.view_teacher_schedule, name="view_teacher_schedule"),
    path('updated_timetable/', views.updated_timetable_view, name='updated_timetable'),
    path("show_second_year_timetable", views.show_second_year_timetable, name="show_second_year_timetable"),
    path("show_third_year_timetable", views.show_third_year_timetable, name="show_third_year_timetable"),
    path("show_fourth_year_timetable", views.show_fourth_year_timetable, name="show_fourth_year_timetable"),
    path('logout/', views.log_out, name='log_out'),
    path('upload', views.upload, name='upload'),
]
