from django.urls import path
from . import views


urlpatterns = [

    path(
        "",
        views.result_list,
        name="result_list"
    ),

    path(
        "add/",
        views.add_result,
        name="add_result"
    ),

    path(
        "<int:pk>/",
        views.result_detail,
        name="result_detail"
    ),

    path(
        "<int:pk>/edit/",
        views.edit_result,
        name="edit_result"
    ),

    path(
        "<int:pk>/delete/",
        views.delete_result,
        name="delete_result"
    ),

]