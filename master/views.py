from django.shortcuts import render
from .models import Tasks
from .forms import NewTaskForm, EditTaskForm, PauseTaskForm
from .databaseWork import DatabaseWork
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import UpdateView
from django.urls import reverse_lazy






@permission_required(perm='master.view_tasks', raise_exception=True)
@login_required
def master_home(request):
  new_task_form = NewTaskForm()
  edit_task_form = EditTaskForm()
  new_paused_form = PauseTaskForm()  
  tasks = Tasks.objects.all().filter(task_is_vision=True).order_by('-id')    
  tasks_stat_all = Tasks.objects.all().count()
  tasks_stat_complited = Tasks.objects.filter(task_status=2).count()  
  load_data = {'title': 'AT-Manager', "task_stat": f'{tasks_stat_all}/{tasks_stat_complited}'}
  print(request.META)
  
  return render(request, 'master.html', {'load_data': load_data, 'new_task_form':new_task_form,
                                         'edit_task_form': edit_task_form, 'new_paused_form':new_paused_form,
                                         'tasks': tasks})

@permission_required(perm='master.change_tasks', raise_exception=True)
@login_required()
def start_task(request):    
  if request.method == 'GET':
    data_task = DatabaseWork({'id_task':request.GET.get('id_task')})
    user_name = f'{request.user.last_name} {request.user.first_name}'
    user_position =f'{request.user.position}'
    task = data_task.push_to_workers(user_name, user_position)     
    if task == True:      
      return HttpResponse('Статус задачи успешно обновлен')
    else:
      return HttpResponse(f'Ошибка обновления задачи: {task}')
  else:
    return HttpResponse('Только GET-запрос')

# Приостановка выполнения задания  
@permission_required(perm='master.change_tasks', raise_exception=True)  
@login_required
def pause_task(request, id_task):   
  if request.method == 'POST':    
    new_paused_form = PauseTaskForm(request.POST)    
    if new_paused_form.is_valid():      
      user_name = f'{request.user.last_name} {request.user.first_name}'
      user_position =f'{request.user.position}'
      new_data_file = DatabaseWork(new_paused_form.cleaned_data)                   
      new_task_file = new_data_file.paused_task(user_name, user_position, id_task)        
      if  new_task_file == True:
        # print(f'Добавление прошло успешно, id записи: {new_data_file.new_task_id}')
        return redirect('/master', permanent=True)
      else:
        return HttpResponse(f'Ошибка: {new_task_file}')
   
# Добавление новой задачи
@permission_required(perm='master.add_tasks', raise_exception=True)
@login_required
def new_task(request):
  if request.method == 'POST':    
    new_task_form = NewTaskForm(request.POST)    
    if new_task_form.is_valid():      
      user_name = f'{request.user.last_name} {request.user.first_name}'
      user_position =f'{request.user.position}'
      new_data_file = DatabaseWork(new_task_form.cleaned_data)
      new_history_file = new_data_file.add_new_history_data(user_name, user_position, new_task_form.cleaned_data['task_comments'])            
      if new_history_file == True:        
        new_task_file = new_data_file.add_new_task_data(user_name)        
        if  new_task_file == True:
          # print(f'Добавление прошло успешно, id записи: {new_data_file.new_task_id}')
          return redirect('/master', permanent=True)
        else:
          return HttpResponse(f'Ошибка: {new_task_file}')
      else:        
        return HttpResponse(f'Ошибка: {new_history_file}')   
\
# Удаление задачи    
@login_required
@permission_required(perm='master.change_tasks', raise_exception=True)  
def delete_task(request):
  if request.method == 'GET':
    data_task = DatabaseWork({'id_task':request.GET.get('id_task')})
    task = data_task.delete_task()     
    if task == True:      
      return HttpResponse('Задача удалена')
    else:
      return HttpResponse(f'Ошибка удаления задачи: {task}') 

# Изменение задачи  
@login_required
@permission_required(perm='master.change_tasks', raise_exception=True)  
def edit_task(request):
  global id_task  
  if request.method == 'GET':
      id_task = request.GET.get('id_task')
      data_task = DatabaseWork({'id_task':request.GET.get('id_task')})
      data = data_task.get_data_from_tasks()      
      return JsonResponse({'task_name': data.task_name, 'task_timedate_start':data.task_timedate_start,
                          'task_timedate_end': data.task_timedate_end, 'task_profile_type': data.task_profile_type_id, 
                          'task_workplace': data.task_workplace_id, 'task_profile_amount': data.task_profile_amount,
                          'task_comments': data.task_comments})
  elif request.method == 'POST':    
    edit_task_form = EditTaskForm(request.POST)    
    if edit_task_form.is_valid():      
      user_name = f'{request.user.last_name} {request.user.first_name}'
      user_position =f'{request.user.position}'
      new_data_file = DatabaseWork(edit_task_form.cleaned_data)
      #new_history_file = new_data_file.add_new_history_data(user_name, user_position)       
      new_task_file = new_data_file.edit_data_from_task(user_name, user_position, id_task)        
      if  new_task_file == True:
        # print(f'Добавление прошло успешно, id записи: {new_data_file.new_task_id}')
        return redirect('/master', permanent=True)
      else:
        return HttpResponse(f'Ошибка: {new_task_file}')
      
  else:
    new_task_form = EditTaskForm() 
    
@login_required
@permission_required(perm='master.change_tasks', raise_exception=True)  
def hide_task(request):
  if request.method == 'GET':
    data_task = DatabaseWork({'id_task':request.GET.get('id_task')})
    task = data_task.hide_task()     
    if task == True:      
      return HttpResponse('Задача скрыта')
    else:
      return HttpResponse(f'Ошибка скрытия задачи: {task}')
  else:
    return HttpResponse('Только GET-запрос')

