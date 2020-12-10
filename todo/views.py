from datetime import datetime, timedelta,date
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import APIException, NotFound, ParseError,PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import pytz
from django.shortcuts import render
from django.utils.timezone import now
from django.utils import timezone
from .serializers import *
from .models import Task,Category
from django.contrib.postgres.search import SearchVector

#Handles retrieving individual tasks and then updating their information and deleting them
class TaskDetailView(APIView):
    def _get_task(self,pk):
        try:
            ret_task = Task.objects.get(id=pk)
        except Task.DoesNotExist:
            raise ParseError("Task does not exist")
        return ret_task

    def _uid_check(self,uid,task_uid):
        if str(uid) != task_uid:
            raise PermissionDenied("You do not have sufficient permissions to view this task")

    def get(self,request,pk):
        user_task  = self._get_task(pk)
        uid = request.user.id
        self._uid_check(uid,user_task.user_id) #checks if token matches current user id
    
        serializer = TaskGetSerializer(user_task)
        return Response(serializer.data,status=200)

    def patch(self,request,pk):
        user_task  = self._get_task(pk)
        uid = request.user.id
        self._uid_check(uid,user_task.user_id) #checks if token matches current user id

        serializer = TaskSerializer(user_task, data=request.data,partial = True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data,status=200)
    
    def delete(self,request,pk):
        user_task  = self._get_task(pk)
        uid = request.user.id
        self._uid_check(uid,user_task.user_id)

        user_task.delete()
        return Response(status=204)

#Handles creating new tasks and retrieving all user tasks based on filter query parameters
class TaskView(APIView):
    def _convert_to_utc(self,due_date):
        est_time = datetime.strptime(due_date, "%Y-%m-%d %H:%M:%S")
        time_zone = pytz.timezone("America/New_York")
        est_time = time_zone.localize(est_time)
        utc_datetime = est_time.astimezone(pytz.utc)
        return utc_datetime

    def _check_due_date(self,due_date):
        if due_date is not None:
            utc_duedate = self._convert_to_utc(due_date)
            if utc_duedate < now():
                raise ParseError("Invalid due date")

    def _check_category(self,cat_id):
        if cat_id is not None:
            try:
                Category.objects.get(id=cat_id)
            except Category.DoesNotExist:
                raise ParseError("Category does not exist")

    def post(self,request):
        request.data._mutable = True
        request.data['user_id'] = request.user.id
        request.data['status'] = 0 #default all tasks are 0 representing pending
        due_date = request.data.get('due_date',None)
        category_id = request.data.get('category',None)
        self._check_due_date(due_date)
        self._check_category(category_id)
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({"detail": "Post Sucessfully added"}, status = 201)

    def get(self,request):
        uid = request.user.id
        category = self.request.query_params.get('category', None)
        status = self.request.query_params.get('status', None)
        all_tasks = Task.objects.filter(user_id=uid)

        self._check_category(category)

        if category!=None and status!=None:
            all_tasks = all_tasks.filter(category=category,status=status)
        elif category!=None and status is None:
            all_tasks = all_tasks.filter(category=category)
        elif category is None and status != None:
            all_tasks = all_tasks.filter(status=status)

        serializer = TaskGetSerializer(all_tasks,many=True)
        return Response(serializer.data,status=200)

#Handles creating new categories and retrieving all categories made by user
class CategoryView(APIView):
    def post(self,request):
        request.data._mutable = True
        request.data['user_id'] = request.user.id
        serializer = CategoryPostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({"detail": "Category Sucessfully added"}, status = 201)

    def get(self,request):
        uid = request.user.id
        all_categories = Category.objects.filter(user_id=uid)
        category_list = CategoryGetSerializer(all_categories,many=True).data
        return Response(category_list,status=200)

#Search through all user tasks with search param looking in both title and description fields
@api_view(['GET'])
def search_tasks(request):
    uid = request.user.id
    search_param = request.query_params['search']
    filtered_task = Task.objects.filter(user_id=uid).annotate(search=SearchVector('title','description')).filter(search__contains =search_param)
    serializer = TaskGetSerializer(filtered_task,many=True)
    return Response(serializer.data,status=200)

