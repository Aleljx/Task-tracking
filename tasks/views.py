from gc import get_objects

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from tasks import models
from django.views.generic import ListView, DetailView, CreateView, View, UpdateView, DeleteView
from tasks.mixins import UserIsOwnerMixin
from tasks.forms import TaskForm
from django.http import HttpResponseRedirect

class TaskListView(ListView):
    model = models.Task
    context_object_name = 'tasks'
    template_name = 'tasks/task_list.html'

class TaskDetailView(DetailView):
    model = models.Task
    context_object_name = 'task'
    template_name = 'tasks/task_detail.html'

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = models.Task
    template_name = 'tasks/task_form.html'
    form_class = TaskForm
    success_url = reverse_lazy('tasks:task_list')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

class TaskCompleteView(LoginRequiredMixin, UserIsOwnerMixin, View):
    def dispatch(self, request, *args, **kwargs):
        task = self.get_object()
        task.status = "done"
        task.save()
        return HttpResponseRedirect(reverse_lazy('tasks:task_list'))

    def get_object(self):
        task_id = self.kwargs.get('pk')
        return get_object_or_404(models.Task, pk=task_id)

class TaskUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = models.Task
    form_class = TaskForm
    template_name = 'tasks/task_update_form.html'
    success_url = reverse_lazy('tasks:task_list')

class TaskDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = models.Task
    success_url = reverse_lazy('tasks:task_list')
    template_name = 'tasks/task_delete_confirmation.html'