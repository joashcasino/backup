from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    # US-16 sign in
    path("login/", views.login_view, name="login"),
    path("after-login/", views.after_login, name="after_login"),
    path("sid/", views.sid_dashboard, name="sid_dashboard"),
]
