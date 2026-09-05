from django.urls import path
from . import views

urlpatterns = [

    path("", views.attendance_list, name="attendance_list"),

    path("add/", views.add_attendance, name="add_attendance"),

    path("<int:pk>/", views.attendance_detail, name="attendance_detail"),

    path("<int:pk>/edit/", views.edit_attendance, name="edit_attendance"),

    path("<int:pk>/delete/", views.delete_attendance, name="delete_attendance"),

]