from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path(
        "",
        views.login_view,
        name="login"
    ),

    path(
        "register/",
        views.register_view,
        name="register"
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),

    path(
        "chatbot/",
        views.chatbot_view,
        name="chatbot"
    ),
    path(
    "forgot-password/",
    auth_views.PasswordResetView.as_view(
        template_name="accounts/password_reset.html"
    ),
    name="password_reset"
),

path(
    "forgot-password/done/",
    auth_views.PasswordResetDoneView.as_view(
        template_name="accounts/password_reset_done.html"
    ),
    name="password_reset_done"
),

path(
    "reset/<uidb64>/<token>/",
    auth_views.PasswordResetConfirmView.as_view(
        template_name="accounts/password_reset_confirm.html"
    ),
    name="password_reset_confirm"
),

path(
    "reset/done/",
    auth_views.PasswordResetCompleteView.as_view(
        template_name="accounts/password_reset_complete.html"
    ),
    name="password_reset_complete"
),

]