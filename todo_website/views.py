from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import TaskForm
from .models import Task
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
# Create your views here.
@login_required
def home(request):
    tasks = Task.objects.all()
    return render(request, 'home.html',
                   {'tasks': tasks}) # pass the tasks to the template

@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = TaskForm()
    return render(request, 'add.html',
                  {'form': form})


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # if registration is successful, it redirects to home
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', { 'form': form })


def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TaskForm(instance=task)
    return render(request, 'edit_task.html', {'form': form, 'task': task})


def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.delete()
    return redirect('home')

def logout_request(request):
    logout(request)
    return redirect("home")