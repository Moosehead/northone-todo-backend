from datetime import datetime, timedelta,date
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import APIException, NotFound, ParseError,PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import pytz
import pdb
from django.shortcuts import render
from django.utils.timezone import now
from django.utils import timezone
from .serializers import *
from .models import Task,Category

from django.contrib.postgres.search import SearchVector

class TaskDetailView(APIView):
    def get_task(self,pk):
        return Task.objects.get(id=pk)

    def uid_check(self,uid,task_uid):
        if str(uid) != task_uid:
            raise PermissionDenied("You do not have sufficient permissions to view this task")

    def get(self,request,pk):
        user_task  = self.get_task(pk)
        uid = request.user.id
        self.uid_check(uid,user_task.user_id)
    
        serializer = TaskGetSerializer(user_task)
        return Response(serializer.data,status=200)

    def patch(self,request,pk):
        user_task  = self.get_task(pk)
        uid = request.user.id
        self.uid_check(uid,user_task.user_id)

        serializer = TaskSerializer(user_task, data=request.data,partial = True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data,status=200)
    
    def delete(self,request,pk):
        user_task  = self.get_task(pk)
        uid = request.user.id
        self.uid_check(uid,user_task.user_id)

        user_task.delete()
        return Response(status=204)


class TaskView(APIView):
    def convert_to_utc(self,due_date):
        est_time = datetime.strptime(due_date, "%Y-%m-%d %H:%M:%S")
        time_zone = pytz.timezone("America/New_York")
        est_time = time_zone.localize(est_time)
        utc_datetime = est_time.astimezone(pytz.utc)
        return utc_datetime

    def post(self,request):
        request.data._mutable = True
        request.data['user_id'] = request.user.id
        request.data['status'] = 0
        due_date = request.data.get('due_date',None)
        if due_date is not None:
            utc_duedate = self.convert_to_utc(due_date)
            if utc_duedate < now():
                raise ParseError("Invalid due date")
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({"detail": "Post Sucessfully added"}, status = 201)

    def get(self,request):
        uid = request.user.id
        category = self.request.query_params.get('category', None)
        status = self.request.query_params.get('status', None)
        all_tasks = Task.objects.filter(user_id=uid)

        if category!=None and status!=None:
            all_tasks = all_tasks.filter(category=category,status=status)
        elif category!=None and status is None:
            all_tasks = all_tasks.filter(category=category)
        elif category is None and status != None:
            all_tasks = all_tasks.filter(status=status)

        serializer = TaskGetSerializer(all_tasks,many=True)
        return Response(serializer.data,status=200)

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


@api_view(['GET'])
def search_tasks(request):
    uid = request.user.id
    search_param = request.query_params['search']
    filtered_task = Task.objects.filter(user_id=uid).annotate(search=SearchVector('title','description')).filter(search__contains =search_param)
    serializer = TaskGetSerializer(filtered_task,many=True)
    return Response(serializer.data,status=200)
