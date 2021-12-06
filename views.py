from django.shortcuts import redirect,render
from django.http import HttpResponse
# Create your views here.
from .filters import OrderFilter
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *
#UserCreation form is built-in form in django, it only has username and password tag
from django.contrib.auth.forms import UserCreationForm
from .forms import *

# Create your views here.
#request.POST is processing the form, to add email field we use user model insteadform = CreateuserForm()
def register(request):
    if request.user.is_authenticated:
        return redirect('list')
    form = CreateuserForm()
    if request.method == 'POST':
        form = CreateuserForm(request.POST)
        if form.is_valid():
            form.save()
            #user = form.cleaned_data.get('username')
            #messages.success(request, "Welcome " + user)
            #after register ,the user will be taken to the signin page automatically
            return redirect('signin')

    return render(request, 'tasks/register.html',{'form':form})

def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,  username = username, password=password)
        if user is not None:
            login(request, user)
            return redirect('list')
        else:
            return HttpResponse('Not Working')

    return render(request,'tasks/signin.html')

def signout(request):
    logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def index(request):
    #model imported straight away into the variable within the views.py function
    tasks = Task.objects.all()
    completed = Task.objects.filter(complete=True).count()
    form = TaskForm()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('list')
    #queryset mentions fields in model, but we select the filtering parameters in the filters.py page
    my_filter = OrderFilter(request.GET, queryset=tasks)
    tasks = my_filter.qs
    context = {'tasks':tasks, 'form':form,'completed':completed,'my_filter':my_filter}
    return render(request, 'tasks/list.html', context)

@login_required(login_url='signin')
def updateTask(request, pk):
    #this will display all model data on html
    task = Task.objects.get(id=pk)
    #this will display input fields through which can add data into the models, this is done via forms.py page
    form = TaskForm(instance=task)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('list')

    context = {'form':form}

    return render(request, 'tasks/update_task.html', context)
@login_required(login_url='signin')
def deleteTask(request, pk):
    item = Task.objects.get(id=pk)

    if request.method == 'POST':
        item.delete()
        return redirect('list')

    context = {'item':item}
    return render(request, 'tasks/delete.html', context)


