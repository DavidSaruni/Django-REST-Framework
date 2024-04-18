from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm, CreateUserForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# rest framework
from rest_framework import response, permissions, viewsets
from rest_framework.decorators import api_view
from .serializers import *
from django.contrib.auth.models import Group, User

# Create your views here.

def Register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'account created for'+ user)
            return redirect('login')
        
    context = {'form':form}
    return render(request, 'accounts/register.html', context)

def LoginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info('Username or Password is incorrect!!')
    context={}
    return render(request, 'accounts/login.html', context)

def LogoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url="login")
def TaskList(request):
    # Get the current user's associated Customer instance
    customer = request.user.customer
    
    # Filter tasks queryset to include only tasks associated with the current user's customer instance
    tasks = Task.objects.filter(user=customer)
    
    form = TaskForm()
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            # Set the user field of the task to the current user's customer instance before saving
            task = form.save(commit=False)
            task.user = customer
            task.save()
            return redirect('/')
    
    context = {'tasks': tasks, 'form': form}
    return render(request, 'base/tasks.html', context=context)

@login_required(login_url="login")
def UpdateTask(request, pk):
    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
        return redirect('/')
    context = {'task':task, 'form':form}
    return render(request, 'base/updatetask.html', context)
        
        
@login_required(login_url="login")
def DeleteTask(request, pk):
    item = Task.objects.get(id=pk)
    if request.method == "POST":
        item.delete()
        return redirect('/')
    context = {'item':item}
    return render(request, 'base/deletetask.html', context)


# api views
@api_view(['GET'])
def getTask(request):
    task = Task.objects.all()
    serializer = TaskSerializer(task, many=True)
    return response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    http://127.0.0.1:8000/api/users/
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    http://127.0.0.1:8000/api/tasks/
    """
    queryset = Task.objects.all().order_by('created_at')
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]