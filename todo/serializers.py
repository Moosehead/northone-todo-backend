from rest_framework import serializers
from .models import Task,Category

class TaskSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length = 500)
    description = serializers.CharField(max_length = 1000)
        
    class Meta:
        model = Task
        fields = ("id","user_id","title","description","status","timestamp","due_date","category_name")

class TaskGetSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField()
    class Meta:
        model = Task
        fields =("id","title","description","status","timestamp","due_date","category_name")

class CategoryPostSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=250)
    class Meta:
        model = Category
        fields = ("id","name","user_id")

class CategoryGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id","name")