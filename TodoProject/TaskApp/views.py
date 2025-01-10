from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from TaskApp.forms import TaskForm
from TaskApp.models import Task
from TaskApp.utils import TitleMixin, FilterMixin, TaskContextMixin

@login_required(login_url="/login/")
def home_view(request) -> HttpResponseRedirect:
    context = {
        'title': 'Home',
        'user': request.user,
    }
    return render(request, 'home.html', context=context)

@login_required(login_url="/login/")
def contacts_view(request) -> HttpResponseRedirect:
    context = {
        'title': 'Contacts',
    }
    return render(request, 'contacts.html', context=context)

@login_required(login_url="/login/")
def info_view(request) -> HttpResponseRedirect:
    context = {
        'title': 'Info',
    }
    return render(request, 'info.html', context=context)

class TaskCreateView(LoginRequiredMixin, TitleMixin, CreateView):
    title = "Task Create"
    model = Task
    form_class = TaskForm
    template_name = 'create_task.html'
    success_url = reverse_lazy('home')
    login_url = '/login/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return redirect('home')

class TaskListView(LoginRequiredMixin, TitleMixin, TaskContextMixin, FilterMixin, ListView):
    title = "Tasks"
    model = Task
    template_name = 'tasks.html'
    context_object_name = 'tasks'
    paginate_by = 10
    login_url = '/login/'

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)
        queryset = self.get_filter_task_data(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class TaskDetailsView(LoginRequiredMixin, TitleMixin, DetailView):
    title = "Task Details"
    model = Task
    template_name = 'details.html'
    context_object_name = 'task'
    login_url = '/login/'

    def get_object(self, queryset=None):
        return get_object_or_404(Task, slug=self.kwargs['slug'], user=self.request.user)

    def post(self, request, *args, **kwargs) -> HttpResponseRedirect:
        task = self.get_object()
        task.done = not task.done
        task.save()
        return redirect('details', slug=task.slug)

class TaskUpdateView(LoginRequiredMixin, TitleMixin, UpdateView):
    title = "Task Update"
    model = Task
    form_class = TaskForm
    template_name = 'update_task.html'
    context_object_name = 'task'
    login_url = '/login/'

    def get_object(self, queryset=None):
        return get_object_or_404(Task, slug=self.kwargs['slug'], user=self.request.user)

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

class TaskDeleteView(LoginRequiredMixin, TitleMixin, DeleteView):
    title = "Task Delete"
    model = Task
    success_url = reverse_lazy('tasks')
    template_name = 'delete_task.html'
    context_object_name = 'task'
    login_url = '/login/'

    def get_object(self, queryset=None):
        return get_object_or_404(Task, slug=self.kwargs['slug'], user=self.request.user)
