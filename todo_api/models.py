from django.db import models
from django.contrib.auth.models import User 

# Create your models here.
# Todo List Fields 
# - task name 
# - status - completed or not 
# - created_at
# - user
# - updated_at
class Todo(models.Model):
    task = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True) # timestamp as when it was created 
    completed = models.BooleanField(default=False, blank=True)
    updated = models.DateTimeField(auto_now = True, blank = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True) # User is built-in Django Model, used as FK
    
    # what does this do? - this is to pretty print object with certain attribute
    def __str__(self):
        return self.task