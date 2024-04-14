from .models import Todo 
from rest_framework import serializers
from djoser.serializers import UserSerializer, UserCreateSerializer as BaseUserSerializer

# serializer for User Object with email, username and password
class UserCreateSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'email', 'username', 'password']

# serializer class to convert Todo object to JSON
class TodoSerializer(serializers.ModelSerializer):
    # overwriting nested class Meta
    class Meta:
        model = Todo
        fields = ["task", "completed", "timestamp", "updated", "user"]