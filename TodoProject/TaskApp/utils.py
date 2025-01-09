from django.views.generic import CreateView

from TaskApp.forms import TaskForm
from TaskApp.models import Task


class TitleMixin:
    title = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context

class TaskCreateView(TitleMixin, CreateView):
    model = Task
    form_class = TaskForm

class FilterMixin:
    def get_filter_task_data(self, queryset):
        title = self.request.GET.get('title', '')
        priority = self.request.GET.get('priority')

        if title:
            queryset = queryset.filter(title__icontains=title)

        if priority:
            queryset = queryset.filter(priority=priority)

        return queryset