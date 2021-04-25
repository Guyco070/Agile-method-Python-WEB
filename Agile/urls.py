"""Agile URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('',views.HomePage, name='homepage'),
    path('SIGNUP',views.SIGNUP, name='SIGNUP'),
    path('LOGIN',views.LOGIN,name='LOGIN'),
    path('SignUpDone',views.SignUpDone,name='SignUpDone'),
    path('LoginStatus',views.LoginStatus,name='LoginStatus'),
    path('AdminHomePage',views.AdminHomePage,name='AdminHomePage'),
    path('ProgrammerHomePage',views.ProgrammerHomePage,name='ProgrammerHomePage'),
    path('ClientHomePage',views.ClientHomePage,name='ClientHomePage'),
    path('NewProjectPage', views.NewProjectPage, name='NewProjectPage'),
    path('CreateProjDone', views.CreateProjDone, name='CreateProjDone'),
    path('showMyProjects',views.showMyProjects,name='showMyProjects'),
    path('ProjectPage',views.ProjectPage,name='ProjectPage'),
    path('ChangeDetailsPage',views.ChangeDetailsPage,name='ChangeDetailsPage'),
    path('updateProjectDetails',views.updateProjectDetails,name='updateProjectDetails'),
    path('KanbanPage',views.KanbanPage,name='KanbanPage'),
    path('AddTasks',views.AddTasks,name='AddTasks'),
    path('ADDTASKS',views.ADDTASKS,name='ADDTASKS'),
    path('taskpage', views.taskpage, name='taskpage'),
    path('taskpage1', views.taskpage1, name='taskpage1'),
    path('taskpage2', views.taskpage2, name='taskpage2'),
    path('taskpage3', views.taskpage3, name='taskpage3'),
    path('EditTasks', views.EditTasks, name='EditTasks'),
    path('TaskPageEdit', views.TaskPageEdit, name='TaskPageEdit'),
    path('TaskPageProgrammer', views.TaskPageProgrammer, name='TaskPageProgrammer'),

]