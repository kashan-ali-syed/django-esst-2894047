from django.urls import path

from . import views

urlpatterns = [
    path("home/", views.HomeView.as_view(), name="home"),
    path("", views.HomeView.as_view(), name="home"),
    path("authorized/", views.AuthorizedView.as_view(), name="home.authorized"),
    path("login/", views.loginInterfaceView.as_view(), name="home.login"),
    path("logout/", views.logoutInterfaceView.as_view(), name="home.logout"),
]
