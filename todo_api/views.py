from django.shortcuts import render
from .models import Todo
from .serializer import TodoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsOwner
# Create your views here.
# function based views vs class based views
# diff/seperate function get, update, deleete vs in class one single clas and add them as class methods

# views
# - view to list all todos
# - add todo which will be form
# - update todo form

# this will help in handling multiple request in one signle class
# /todo/get --> TodoListView.get()
# /todo/create -> TodoListView.create()


# HTTP STATUS CODES - Server sending Response
# 200 - Request is successfull
# 404 - URL/Page is not found
# 500 - Server Side Error
# 201 - Object has been created successfully

# Method Names in class view
# Get all objects - get()
# Create new object - post()
# Update object - put()
# Delete object - delete()


# Serializer is used to convert Python Class Object to JSON and vice-versa i.e JSON to Python Class Object
# Python Class Object to JSON - sending response
# JSON to Python Class Object - getting request input


class TodoListView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    authentication_classes = [JWTAuthentication]

    # get all todolist
    def get(self, request, *args, **kwargs):
        todos = Todo.objects.filter(
            user=request.user.id
        )  # filtering based on which user has created
        serializer = TodoSerializer(todos, many=True)# many=true is specifying that todos might multiple items inside it
        return Response(serializer.data, status=status.HTTP_200_OK)

    # creating new object
    def post(self, request, *args, **kwargs):
        data = {
            "task": request.data.get("task"),
            "completed": request.data.get("completed"),
            "user": request.user.id,
        }
        serializer = TodoSerializer(data=data)
        # type of serializer is Python Class Object
        if serializer.is_valid():  # returns True/False after fields check
            serializer.save()  # this will update the db by inserting a new todo object
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TodoDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    authentication_classes = [JWTAuthentication]

    def get_object_by_id(self, todo_id, user_id):
        try:
            return Todo.objects.get(id=todo_id, user_id=user_id)
        except Todo.DoesNotExist:
            return None

    # to get a single todo object
    def get(self, request, todo_id, *args, **kwargs):
        todo_object = self.get_object_by_id(todo_id, request.user.id)
        if todo_object:
            serializer = TodoSerializer(todo_object)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"res": "Todo Object does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    # to update single todo object
    def put(self, request, todo_id, *args, **kwargs):
        todo_object = self.get_object_by_id(todo_id, request.user.id) # existing object
        if todo_object:
            updated_data = {
                "task": request.data.get("task"),
                "completed": request.data.get("completed"),
                "user": request.user.id,
            }
            serializer = TodoSerializer(
                instance=todo_object, data=updated_data, partial=True
            )  # not updating entire object, pass keyword called partial = True
            if serializer.is_valid():
                serializer.save()  # this will save object in db
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(
                {"res": "Todo Object does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    # to delete single todo object
    def delete(self, request, todo_id, *args, **kwargs):
        todo_object = self.get_object_by_id(todo_id, request.user.id)
        if not todo_object:
                return Response(
                {"res": "Object with todo id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        todo_object.delete()
        return Response(
                {"res": f"Todo Object of id {todo_id} Deleted"},
                status=status.HTTP_200_OK,
            )

# add, commit, push, pull, fetch, remote, branch, status
# tracked and untracked files
# staged and unstaged 
