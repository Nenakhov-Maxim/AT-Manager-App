from .models import *
import datetime

class DatabaseWork:
  def __init__ (self, data):
    self.data = data
    self.history_id = -1
    self.new_task_id = -1
  
  
  # Добавить новую задачу (мастер)  
  def add_new_task_data(self, user_name):
    try:            
      new_task = Tasks.objects.create(
        task_name = self.data['task_name'],
        task_timedate_start = self.data['task_timedate_start'],
        task_timedate_end = self.data['task_timedate_end'],
        task_profile_type_id = self.data['task_profile_type'].id,
        task_workplace_id = self.data['task_workplace'].id,
        task_profile_amount = self.data['task_profile_amount'],
        task_comments = self.data['task_comments'],
        task_status_id = 1,
        task_user_created = user_name,
        task_history_id = self.history_id
        )
      self.new_task_id = new_task.id
      return True
    except Exception as e:
      return f'Ошибка создания новой задачи: {e}'
  
  # Добавить новое значение в лог задачи
  def add_new_history_data(self,user_name, user_position, comment):
    now = datetime.datetime.now()
    try:
      history_task = Task_history.objects.create(history_name={1:f"{now};Задача создана;{user_position} - {user_name}, комментарий: {comment}"})
      self.history_id = history_task.id      
      return True
    except Exception as e:
      return f'Ошибка создания истории: {e}'
  
  # Отправить задачу на выпонение рабочему (мастер) 
  def push_to_workers(self, user_name, user_position):
    now = datetime.datetime.now()
    task = Tasks.objects.get(id=self.data['id_task'])
    history_task = Task_history.objects.get(id=task.task_history_id)    
    new_event = history_task.history_name
    max_key = max(new_event, key=new_event.get)
    new_event[int(max_key) + 1] = f'{now};Отправлена рабочему;{user_position} - {user_name}'
    history_check = [False, '']
    try:
      history_task.history_name = new_event
      history_task.save(update_fields=['history_name'])
      history_check = [True, '']            
    except Exception as e:
      history_check = [False, f'Ошибка изменения истории: {e}']    
    
    if history_check[0] ==  True:      
      try:
        task.task_status_id = 4
        task.save(update_fields=['task_status_id'])
        return  True
      except Exception as e:
        return f'Ошибка изменения статуса задачи: {e}'
    else:
      return history_check[1]
  
  # Приостановить выполнение задачи (мастер, рабочий)
  def paused_task(self, user_name, user_position, id_task):
    now = datetime.datetime.now()
    task = Tasks.objects.get(id=id_task)
    history_task = Task_history.objects.get(id=task.task_history_id)
    new_event = history_task.history_name
    max_key = max(new_event, key=new_event.get)
    new_event[int(max_key) + 1] = f"{now};Задача приостановлена;{user_position} - {user_name}, категория проблемы: {self.data['problem_type']}, комментарий: {self.data['problem_comments']}"
    history_check = [False, '']
    try:
      history_task.history_name = new_event
      history_task.save(update_fields=['history_name'])
      history_check = [True, '']            
    except Exception as e:
      history_check = [False, f'Ошибка изменения истории: {e}']    
    
    if history_check[0] ==  True:      
      try:
        task.task_status_id = 6
        task.save(update_fields=['task_status_id'])
        return  True
      except Exception as e:
        return f'Ошибка изменения статуса задачи: {e}'
    else:
      return history_check[1]
  
  # Удалить задачу (мастер) 
  def delete_task(self):
    try:
      task = Tasks.objects.get(id=self.data['id_task'])
      history_task = Task_history.objects.get(id=task.task_history_id)
      task.delete()
      history_task.delete()
    except Exception as e:
       return f'Ошибка удаления задачи: {e}'
  
  # Получить данные по задаче   
  def get_data_from_tasks(self):
    try:
      task = Tasks.objects.get(id=self.data['id_task'])     
      return task
    except Exception as e:
      return f'Ошибка удаления задачи: {e}'
  
  # Изменить задачу (Мастер)
  def edit_data_from_task(self, user_name, user_position, id_task):
    now = datetime.datetime.now()  
    task = Tasks.objects.get(id=id_task)
    history_task = Task_history.objects.get(id=task.task_history_id)
    new_event = history_task.history_name
    max_key = max(new_event, key=new_event.get)
    new_event[int(max_key) + 1] = f'{now};Задача отредактирована;{user_position} - {user_name}'
    history_check = [False, '']
    try:
      history_task.history_name = new_event
      history_task.save(update_fields=['history_name'])
      history_check = [True, '']            
    except Exception as e:
      history_check = [False, f'Ошибка изменения истории: {e}']
    
    if history_check[0] ==  True:      
      try:
        number = Tasks.objects.filter(id=id_task).update(
        task_name = self.data['task_name'],
        task_timedate_start = self.data['task_timedate_start'],
        task_timedate_end = self.data['task_timedate_end'],
        task_profile_type_id = self.data['task_profile_type'].id,
        task_workplace_id = self.data['task_workplace'].id,
        task_profile_amount = self.data['task_profile_amount'],
        task_comments = self.data['task_comments'],
        task_timedate_start_fact = None     
      )
        print(number) # количество обновленных строк
        return  True
      except Exception as e:
        return f'Ошибка изменения статуса задачи: {e}'
    else:
      return history_check[1]
  
  # Старт выполнения работы рабочим  
  def start_working(self, id_task, user_name, user_position):
    # Получаем запись задачи, ее истории
    now = datetime.datetime.now()  
    task = Tasks.objects.get(id=id_task)
    history_task = Task_history.objects.get(id=task.task_history_id)
    # генерируем новою запись в истории
    new_event = history_task.history_name
    max_key = max(new_event, key=new_event.get)
    new_event[int(max_key) + 1] = f'{now};Старт выполнения задачи;{user_position} - {user_name}, фактическое время начала - {now}'
    history_check = [False, '']
    # пробуем переписать историю
    try:
      history_task.history_name = new_event
      history_task.save(update_fields=['history_name'])
      history_check = [True, '']            
    except Exception as e:
      history_check = [False, f'Ошибка изменения истории: {e}']
    #  пробуем изменить статус и фактическое время начала задачи     
    if history_check[0] ==  True:      
      try:
        number = Tasks.objects.filter(id=id_task).update(        
        task_timedate_start_fact = now,
        task_status_id = 3     
      )
        print(number) # количество обновленных строк
        return  True
      except Exception as e:
        return f'Ошибка изменения статуса задачи: {e}'
    else:
      return history_check[1] 
    
  # Отмена выполнения работы рабочим  
  def deny_task(self, user_name, user_position, id_task):
    now = datetime.datetime.now()
    task = Tasks.objects.get(id=id_task)
    history_task = Task_history.objects.get(id=task.task_history_id)
    new_event = history_task.history_name
    max_key = max(new_event, key=new_event.get)
    new_event[int(max_key) + 1] = f"{now};Выполнение задачи невозможно;{user_position} - {user_name}, категория проблемы: {self.data['problem_type']}, комментарий: {self.data['problem_comments']}"
    history_check = [False, '']
    try:
      history_task.history_name = new_event
      history_task.save(update_fields=['history_name'])
      history_check = [True, '']            
    except Exception as e:
      history_check = [False, f'Ошибка изменения истории: {e}']    
    
    if history_check[0] ==  True:      
      try:
        task.task_status_id = 5
        task.save(update_fields=['task_status_id'])
        return  True
      except Exception as e:
        return f'Ошибка изменения статуса задачи: {e}'
    else:
      return history_check[1]
    
  # Скрыть задачу (мастер)
  def hide_task(self):
    task = Tasks.objects.get(id=self.data['id_task'])
    try:
        task.task_is_vision = False
        task.save(update_fields=['task_is_vision'])
        return  True
    except Exception as e:
        return f'Ошибка изменения статуса задачи: {e}'
      
  # Завершение задачи
  def complete_task(self, id_task, user_name, user_position):
    now = datetime.datetime.now()
    task = Tasks.objects.get(id=id_task)
    history_task = Task_history.objects.get(id=task.task_history_id)
    new_event = history_task.history_name
    max_key = max(new_event, key=new_event.get)
    new_event[int(max_key) + 1] = f"{now};Задача № {id_task} выполнена;{user_position} - {user_name}, фактическое время выполнения - {now}"
    history_check = [False, '']
    try:
      history_task.history_name = new_event
      history_task.save(update_fields=['history_name'])
      history_check = [True, '']            
    except Exception as e:
      history_check = [False, f'Ошибка изменения истории: {e}']    
    
    if history_check[0] ==  True:      
      try:
        task.task_status_id = 2
        task.task_timedate_end_fact = now
        task.save(update_fields=['task_status_id', 'task_timedate_end_fact'])
        return  True
      except Exception as e:
        return f'Ошибка завершения задачи: {e}'
    else:
      return history_check[1]
    
  # Старт переналадки
  def start_settingUp(self, id_task, user_name):
    pass
     