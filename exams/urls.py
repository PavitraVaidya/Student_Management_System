from django.urls import path
from . import views


urlpatterns = [

    path(
        "",
        views.exam_list,
        name="exam_list"
    ),

    path(
        "add/",
        views.add_exam,
        name="add_exam"
    ),

    path(
        "<int:pk>/",
        views.exam_detail,
        name="exam_detail"
    ),

    path(
        "<int:pk>/edit/",
        views.edit_exam,
        name="edit_exam"
    ),

    path(
        "<int:pk>/delete/",
        views.delete_exam,
        name="delete_exam"
    ),

]