from rest_framework import serializers
from .models import Task,Category

# def date_check(dob):
#     today = date.today()
#     age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
#     if (not(20 < age < 30)):
#         raise serializers.ValidationError("You are no eligible for the job")
#     return dob

class TaskSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length = 500)
    description = serializers.CharField(max_length = 1000)
    # due_date = serializers.SerializerMethodField('get_classification',validators=[date_check])

    # def get_due_date(self, obj):
    #     return getattr(obj, 'due_date', None)
        
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