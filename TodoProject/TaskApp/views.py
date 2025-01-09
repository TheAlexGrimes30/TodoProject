from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

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
    template_name = 'tasks.html'
    context_object_name = 'tasks'
    paginate_by = 10

    def get_queryset(self):
        queryset = Task.objects.all()
        queryset = self.get_filter_task_data(queryset)
        return queryset

class TaskDetailsView(TitleMixin, DetailView):
    title = "Task Details"
    model = Task
    template_name = 'details.html'
    context_object_name = 'task'

    def get_object(self, queryset=None):
        return get_object_or_404(Task, slug=self.kwargs['slug'])

class TaskUpdateView(TitleMixin, UpdateView):
    title = "Task Update"
    model = Task
    form_class = TaskForm
    template_name = 'update_task.html'
    context_object_name = 'task'

    def get_object(self, queryset=None):
        return get_object_or_404(Task, slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.get_object()
        context['task'] = task
        return context

    def form_valid(self, form):
        task = form.save(commit=False)
        task.save()
        return redirect(reverse_lazy('details', kwargs = {'slug': task.slug}))

    def get_success_url(self):
        return reverse_lazy('details', kwargs={'slug': self.kwargs['slug']})

class TaskDeleteView(TitleMixin, DeleteView):
    title = "Task Delete"
    model = Task
    success_url = reverse_lazy('tasks')
    template_name = 'delete.html'
    context_object_name = 'task'
