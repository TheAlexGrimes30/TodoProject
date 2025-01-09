from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from TaskApp.forms import TaskForm
from TaskApp.models import Task
from TaskApp.utils import TitleMixin, FilterMixin, TaskContextMixin


def home_view(request) -> HttpResponseRedirect:
    context = {
        'title': 'Home',
        'user': request.user,
    }
    return render(request, 'home.html', context=context)

def contacts_view(request) -> HttpResponseRedirect:
    context = {
        'title': 'Contacts',
    }
    return render(request, 'contacts.html', context=context)

def info_view(request) -> HttpResponseRedirect:
    context = {
        'title': 'Info',
    }
    return render(request, 'info.html', context=context)

class TaskCreateView(TitleMixin, CreateView):
    title = "Task Create"
    model = Task
    form_class = TaskForm
    template_name = 'create_task.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.save()
        return redirect('home')

class TaskListView(TitleMixin, TaskContextMixin, FilterMixin, ListView):
    title = "Tasks"
    model = Task
    template_name = 'list_task.html'
    context_object_name = 'tasks'
    paginate_by = 10

    def get_queryset(self):
        queryset = Task.objects.all()
        queryset = queryset.get_filter_task_data(queryset)
        return queryset



