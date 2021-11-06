from django.db import models
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
"""use to redirect to a different part of our page or app"""
from .models import Task

# Create your views here.
class TaskList(ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'base/task_list.html'

class TaskDetail(DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task_detail.html'

class TaskCreate(CreateView):
    model = Task
    fields = '__all__'     
    """If you wanna get the fields specifically, you use fields = ['title', 'description', etc.]"""
    success_url = reverse_lazy('tasks')
    """It is sending to the url named tasks, which is this one
    path('', views.TaskList.as_view(), name="tasks") (the first url)"""
    template_name = 'base/task_form.html'

class TaskUpdate(UpdateView):
    model = Task
    fields = '__all__'     
    success_url = reverse_lazy('tasks')
    template_name = 'base/task_form.html'
    """That's the default template name"""

class TaskDelete(DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    template_name = 'base/task_confirm_delete.html'
    """That's the default template name"""