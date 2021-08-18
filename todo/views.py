from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.


def home(request):
    return render(request, 'todo/home.html')


def signupUser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupUser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currentTodos')

            except IntegrityError:
                return render(request, 'todo/signupUser.html', {'form': UserCreationForm(), 'error': 'That username is alredy taken'})
        else:
            #Tell the user
            return render(request, 'todo/signupUser.html', {'form': UserCreationForm(), 'error': 'Passwords did not match'})


@login_required
def currentTodos(request):
    todos = Todo.objects.filter(user=request.user, date_completed__isnull=True)
    return render(request, 'todo/currentTodos.html', {'todos': todos})


@login_required
def completedTodos(request):
    todos = Todo.objects.filter(user=request.user, date_completed__isnull=False).order_by('-date_completed')
    return render(request, 'todo/completedTodos.html', {'todos': todos})


@login_required
def viewTodos(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/viewTodos.html', {'todo': todo, 'form': form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currentTodos')
        except ValueError:
            return render(request, 'todo/viewTodos.html', {'todo': todo, 'form': form, 'error': 'Bad info'})


@login_required
def completeTodos(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.date_completed = timezone.now()
        todo.save()
        return redirect('currentTodos')


@login_required
def deleteTodos(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currentTodos')


@login_required
def logoutUser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def loginUser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginUser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginUser.html', {'form': AuthenticationForm(), 'error': 'Username and password did not match'})
        else:
            login(request, user)
            return redirect('currentTodos')


@login_required
def createTodos(request):
    if request.method == 'GET':
        return render(request, 'todo/createTodos.html', {'form': TodoForm()})        
    else:
        try:
            form = TodoForm(request.POST)
            newTodo = form.save(commit=False)
            newTodo.user = request.user
            newTodo.save()
            return redirect('currentTodos')
        except ValueError:
            return render(request, 'todo/createTodos.html', {'form': TodoForm(), 'error': 'Bad data passed in'})    