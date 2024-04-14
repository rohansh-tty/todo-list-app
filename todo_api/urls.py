# Serializer ---> used to convert your custom class Python object to JSON format
# JSON is format in which you represent data and is supported by all languags
from django.urls import path, include
from .views import TodoListView, TodoDetailView

app_name = "polls"

urlpatterns = [
    path('api', TodoListView.as_view()), 
    path('api/<int:todo_id>/', TodoDetailView.as_view())
]
# 127.0.0.1:8000/todo/api/, GET/PUT/POST