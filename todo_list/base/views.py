from django.db import models
from django.shortcuts import redirect, render
from django.urls.base import reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView


from django.urls import reverse_lazy
"""use to redirect to a different part of our page or app"""
from django.contrib.auth.views import LoginView

from django.contrib.auth.mixins import LoginRequiredMixin
"""If you wanna restricted a class if the user isn't logged in, just put the view you want to restrict

then you gotta go to settings.py and add this at the end to set 

LOGIN_URL = 'login'

"""

from django.contrib.auth.forms import UserCreationForm
"""Once we create a user we want to log that user in directly so we can don't want to force them to log in"""
from django.contrib.auth import login


from .models import Task

# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    """If the use is logged in, it will be redirected to taks url"""
    def get_success_url(self):
        return reverse_lazy('tasks')

class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        """Once it's created, you're logged in with this"""
        user = form.save()
        if user is not None:
            login(self.request, user)
            """This authenticate the user"""
        return super(RegisterPage, self).form_valid(form)
        
    """If you're logged in, you can't see this page"""
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'base/task_list.html'
    
    """Function to make sure the user only sees his data"""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()


        search_input = self.request.GET.get('search-area') or ''
        """search area is the name of the input and or means if we don't search anything, the field is going to be blank"""
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)
            """you can use startswith if you wanna get the values if the word starts with that"""
    
        context['search_input'] = search_input
        return context

class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task_detail.html'

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    """Delete __all__ so the user can't create tasks in another user """
    fields = ['title', 'description', 'complete']    
    """If you wanna get the fields specifically, you use fields = ['title', 'description', etc.]"""
    success_url = reverse_lazy('tasks')
    """It is sending to the url named tasks, which is this one
    path('', views.TaskList.as_view(), name="tasks") (the first url)"""
    template_name = 'base/task_form.html'

    """Function to prevent other users to create tasks in other users"""
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)
    
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']     
    success_url = reverse_lazy('tasks')
    template_name = 'base/task_form.html'
    """That's the default template name"""

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    template_name = 'base/task_confirm_delete.html'
    """That's the default template name"""