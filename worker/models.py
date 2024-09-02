from django.db import models

class WorkerTypeProblem(models.Model):
  name_problem = models.CharField('Наименование типа проблемы', max_length=100)
  
  def __str__(self):
    return str(self.name_problem) 
