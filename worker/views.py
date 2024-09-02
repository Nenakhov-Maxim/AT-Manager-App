from django.shortcuts import render
from master.models import *
from master.databaseWork import DatabaseWork
from django.http import HttpResponse, JsonResponse
from .forms import PauseTaskForm, DenyTaskForm
import datetime
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import cv2
import threading
from ultralytics import YOLO
import asyncio
from django.views.decorators.csrf import csrf_exempt

# Стратовая страница
@login_required
@permission_required(perm='worker.change_workertypeproblem', raise_exception=True) 
def worker_home(request, filter='all'):
  new_paused_form = PauseTaskForm()
  new_deny_form = DenyTaskForm()  
  now = datetime.datetime.now()
  area_id = request.user.production_area_id
  tasks = Tasks.objects.all().filter(task_workplace=area_id, task_status_id__in=[3, 4])
  task_to_start = tasks.filter(task_status_id=4).count
  task_start= tasks.filter(task_status_id=3).count
  user_info = [request.user.first_name, request.user.last_name, request.user.position, request.user.production_area_id]
  if filter == 'now':
    tasks = tasks.filter(task_timedate_start__lte = now)
  elif filter == 'week':    
    tasks = tasks.filter(task_timedate_start__lte = now + datetime.timedelta(days=5))
  elif filter == 'month':    
    tasks = tasks.filter(task_timedate_start__lte = now + datetime.timedelta(days=30))
  
  return render(request, 'worker.html', {'filter': filter, 'tasks':tasks, 'task_to_start':task_to_start,
                                         'task_start':task_start, 'user_info':user_info, 'new_paused_form':new_paused_form,
                                         'new_deny_form':new_deny_form})

# Запуск задания в работу
@login_required
@permission_required(perm='worker.change_workertypeproblem', raise_exception=True) 
def start_working(request):
  if request.method == 'GET':
    # Получаем id задачи
    id_task = request.GET.get('id_task')
    user_name = f'{request.user.last_name} {request.user.first_name}'
    user_position = request.user.position
    data_task = DatabaseWork({'id_task':id_task})
    result = data_task.start_working(id_task, user_name, user_position)
    
    return HttpResponse(result)
  
# Изменение фильтра-меню(сегодня)
@login_required
@permission_required(perm='worker.change_workertypeproblem', raise_exception=True)   
def task_now(request):
  filter = 'now'
  return_value = worker_home(request, filter)
  
  return return_value

# Изменение фильтра-меню(неделя)
@login_required
@permission_required(perm='worker.change_workertypeproblem', raise_exception=True) 
def task_week(request):
  filter = 'week'
  return_value = worker_home(request, filter)
  
  return return_value

# Изменение фильтра-меню (месяц)
@login_required
@permission_required(perm='worker.change_workertypeproblem', raise_exception=True) 
def task_month(request):
  filter = 'month'
  return_value = worker_home(request, filter)
  
  return return_value

# Приостановка выполнения задания
@login_required
@permission_required(perm='worker.change_workertypeproblem', raise_exception=True) 
def pause_task(request):  
  global id_task  
  if request.method == 'POST':    
    new_paused_form = PauseTaskForm(request.POST)    
    if new_paused_form.is_valid():      
      user_name = f'{request.user.last_name} {request.user.first_name}'
      user_position =f'{request.user.position}'
      new_data_file = DatabaseWork(new_paused_form.cleaned_data)                   
      new_task_file = new_data_file.paused_task(user_name, user_position, id_task)        
      if  new_task_file == True:      
        return redirect('/worker', permanent=True)
      else:
        return HttpResponse(f'Ошибка: {new_task_file}')
  elif request.method == 'GET':
    id_task = request.GET.get('id_task')    
    return HttpResponse(f'Данные отправлены на сервер, id записи: {id_task}') 
  else:
    new_task_form = PauseTaskForm()

# Отмена выполнения задания
@login_required
@permission_required(perm='worker.change_workertypeproblem', raise_exception=True)     
def deny_task(request):
  global id_task  
  if request.method == 'POST':    
    new_deny_form = DenyTaskForm(request.POST)    
    if new_deny_form.is_valid():      
      user_name = f'{request.user.last_name} {request.user.first_name}'
      user_position =f'{request.user.position}'
      new_data_file = DatabaseWork(new_deny_form.cleaned_data)                   
      new_task_file = new_data_file.deny_task(user_name, user_position, id_task)        
      if  new_task_file == True:
        
        return redirect('/worker', permanent=True)
      else:
        
        return HttpResponse(f'Ошибка: {new_task_file}')
  elif request.method == 'GET':
    id_task = request.GET.get('id_task') 
       
    return HttpResponse(f'Данные отправлены на сервер, id записи: {id_task}') 
  else:
    new_task_form = DenyTaskForm()

# Завершение задачи
@login_required
@permission_required(perm='worker.change_workertypeproblem', raise_exception=True)   
def complete_task(request):  
  if request.method == 'GET':    
    # Получаем id задачи
    id_task = request.GET.get('id_task')
    user_name = f'{request.user.last_name} {request.user.first_name}'
    user_position = request.user.position
    data_task = DatabaseWork({'id_task':id_task})
    result = data_task.complete_task(id_task, user_name, user_position)
       
    return HttpResponse(result)