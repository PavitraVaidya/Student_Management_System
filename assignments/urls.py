from django.urls import path
from . import views


urlpatterns = [

    path(
        "",
        views.assignment_list,
        name="assignment_list"
    ),

    path(
        "add/",
        views.add_assignment,
        name="add_assignment"
    ),

    path(
        "<int:pk>/",
        views.assignment_detail,
        name="assignment_detail"
    ),

    path(
        "<int:pk>/edit/",
        views.edit_assignment,
        name="edit_assignment"
    ),

    path(
        "<int:pk>/delete/",
        views.delete_assignment,
        name="delete_assignment"
    ),

]