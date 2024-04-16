from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm #UserCreationForm Para crear formulario de autenticación
                                                       # AuthenticationForm formulario de logueo
from django.contrib.auth.models import User #se importa el modelo usur de Django
from django.contrib.auth import login, logout, authenticate #para crear y validad la sesion y logout para cerrar sesion
                                                            # authenticate para logueo de usuarios
from .forms import TaskForm
from .models import Task
from django.utils import timezone # funciones de hora y fecyha
from django.contrib.auth.decorators import login_required #Para proteger las rutas

# Create your views here.
def home(request):
    return render(request, 'home.html')

def signup(request):
    print('bien 12')
    if request.method == 'GET':
       print('bien')
       return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            #registrar usurios
            try:
                user = User.objects.create_user(username=request.POST['username'], 
                                                password=request.POST['password1'])
                user.save()
                #crea la sesion del usuario
                login(request, user)
                return redirect('tasks')
            except:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'UserName already exist'
                })
            
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'password don not match'
        })


@login_required    
def tasks(request):
    # consulta las tareas 
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'task.html', {
        'tasks': tasks
    })

@login_required    
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id)
        form = TaskForm(instance=task)
       
        return render(request, 'task_detail.html', {
            'task': task,
            'form': form
        })
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user = request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        
        except ValueError:
            task = get_object_or_404(Task, pk=task_id, user = request.user)
            form = TaskForm(instance=task)
        
            return render(request, 'task_detail.html', {
                'task': task,
                'form': form,
                'error': 'Error updating task'
            })
            

@login_required
def task_complete(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user = request.user)
    task.datecompleted = timezone.now()
    task.save()
    return redirect('tasks')


@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user = request.user)
    task.delete()
    return redirect('tasks')
        


@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
    else:
        try:
            # crea un formiulario capturando los datos enviados por el request
            form = TaskForm(request.POST)
            # crea una nueva tarea con el form.save, se le pas como parametro commit = false para que no lo guarde
            # solo toma los datos
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
                'form': TaskForm,
                'error': 'Please provided correct dates'
            })
        

@login_required
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    print(request.POST)
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        print(user)
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Username or password incorrect'
            })
        else:
            login(request, user)
            return redirect('tasks')
            
        
    
