"""
URL configuration for TodoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path

from AuthApp.views import RegistrationView, CustomLoginView, UserProfile, CustomLogoutView, UserProfileUpdateView, \
    UserProfileDeleteView
from TaskApp.views import home_view, contacts_view, info_view, TaskCreateView, TaskListView, TaskUpdateView, \
    TaskDeleteView, TaskDetailsView

urlpatterns = [
    path('', home_view, name='home'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('contacts/', contacts_view, name='contacts'),
    path('info/', info_view, name='info'),
    path('profile/<int:id>', UserProfile.as_view(), name='profile'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('profile/<int:id>/update-profile', UserProfileUpdateView.as_view(), name='profile_update'),
    path('profile/<int:id>/delete-profile', UserProfileDeleteView.as_view(), name='profile_delete'),
    path('create-task/', TaskCreateView.as_view(), name='task_create'),
    path('tasks/', TaskListView.as_view(), name="tasks"),
    path('tasks/<slug:slug>/details/', TaskDetailsView.as_view(), name="details"),
    path('tasks/<slug:slug>/details/update/', TaskUpdateView.as_view(), name="task_update"),
    path('tasks/<slug:slug>/details/delete/', TaskDeleteView.as_view(), name='task_delete'),
]
