from django.urls import path
from . import views

urlpatterns = [
    # authentication
    path('register', views.Register, name="register"),
    path('login', views.LoginPage, name="login"),
     path('logout', views.LogoutUser, name="logout"),

    path('', views.TaskList, name="taskslist"),
    path('updatetask/<str:pk>', views.UpdateTask, name="updatetask"),
    path('deletetask/<str:pk>', views.DeleteTask, name="deletetask"),


]