from django.urls import path
from . import views

urlpatterns = [

    path("", views.teacher_list, name="teacher_list"),

    path("add/", views.add_teacher, name="add_teacher"),

    path("<int:pk>/", views.teacher_detail, name="teacher_detail"),

    path("<int:pk>/edit/", views.edit_teacher, name="edit_teacher"),

    path("<int:pk>/delete/", views.delete_teacher, name="delete_teacher"),

]