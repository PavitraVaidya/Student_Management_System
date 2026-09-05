from django.urls import path
from . import views


urlpatterns = [

    path(
        "",
        views.fee_list,
        name="fee_list"
    ),

    path(
        "add/",
        views.add_fee,
        name="add_fee"
    ),

    path(
        "<int:pk>/",
        views.fee_detail,
        name="fee_detail"
    ),

    path(
        "<int:pk>/edit/",
        views.edit_fee,
        name="edit_fee"
    ),

    path(
        "<int:pk>/delete/",
        views.delete_fee,
        name="delete_fee"
    ),

]