import urllib
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.test import force_authenticate
from datetime import datetime, timedelta,date
from django.utils.timezone import now
from ..models import Task,Category

class TaskCreationTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('user1', 'user@gmail.com', 'user123')
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_createTask(self):
        body_data = {'title':'task1','description':'task1 desc'}
        task_data =urllib.parse.urlencode(body_data) 
        self.client.force_login(user=self.user)
        response = self.client.post('/api/task', data=task_data,content_type='application/x-www-form-urlencoded')
        self.assertEqual(response.status_code, 201)
    
    def test_createInvalidDateTask(self):
        body_data = {'title':'task1','description':'task1 desc','due_date':'2020-12-02 09:15:32'}
        task_data =urllib.parse.urlencode(body_data) 
        self.client.force_login(user=self.user)
        response = self.client.post('/api/task', data=task_data,content_type='application/x-www-form-urlencoded')
        self.assertEqual(response.status_code, 400)

class TaskRetrievalTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('user1', 'user@gmail.com', 'user123')
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()
        self.total_tasks=4

        category_1 = Category.objects.create(
            name='category1',user_id=self.user.id, id= 1
        )

        category_2 = Category.objects.create(
            name='category2',user_id=self.user.id, id =2
        )

        Task.objects.create(
            title='task1',description='task1 description',user_id=self.user.id,category=category_1,due_date=now() + timedelta(days=7)
        )

        Task.objects.create(
            title='task2',description='task2 description',user_id=self.user.id,category=category_1,due_date=now() + timedelta(days=7)
        )

        Task.objects.create(
            title='task3',description='task3 description',user_id=self.user.id,category=category_1,due_date=now() + timedelta(days=7),status = 1
        )

        Task.objects.create(
            title='task4',description='task4 description',user_id=self.user.id,category=category_2,due_date=now() + timedelta(days=7),status = 1
        )
    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_checkResponse(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/api/task')
        self.assertEqual(response.status_code, 200)

    def test_checkAllContents(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/api/task')
        self.assertEqual(len(response.data), self.total_tasks)

    def test_checkCompleted(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/api/task?status=1')
        self.assertEqual(len(response.data), 2)

    def test_checkCategory(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/api/task?category=2')
        self.assertEqual(len(response.data), 1)

    def test_checkCategoryAndCompleted(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/api/task?status=1&category=2')
        self.assertEqual(len(response.data), 1)

class UpdateTaskTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('user1', 'user@gmail.com', 'user123')
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

        category_1 = Category.objects.create(
            name='category1',user_id=self.user.id, id= 1
        )

        category_2 = Category.objects.create(
            name='category2',user_id=self.user.id, id =2
        )

        Task.objects.create(
            id=1,title='task1',description='task1 description',user_id=self.user.id,category=category_1,due_date=now() + timedelta(days=7)
        )

        Task.objects.create(
            id=2,title='task2',description='task2 description',user_id=self.user.id,category=category_1,due_date=now() + timedelta(days=7)
        )

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_updateTaskStatus_responseCheck(self):
        body_data = {'status':1}
        task_data =urllib.parse.urlencode(body_data) 
        response = self.client.patch('/api/task/1', data=task_data,content_type='application/x-www-form-urlencoded')
        self.assertEqual(response.status_code, 200)

    def test_updateTaskStatus_statusCheck(self):
        body_data = {'status':1}
        task_data =urllib.parse.urlencode(body_data) 
        response = self.client.patch('/api/task/2', data=task_data,content_type='application/x-www-form-urlencoded')
        self.assertEqual(response.data['status'], 1)

    def test_checkCompleted(self):
        body_data = {'status':1}
        task_data =urllib.parse.urlencode(body_data) 
        self.client.patch('/api/task/1', data=task_data,content_type='application/x-www-form-urlencoded')
        self.client.patch('/api/task/2', data=task_data,content_type='application/x-www-form-urlencoded')
        response = self.client.get('/api/task?status=1')
        self.assertEqual(len(response.data), 2)

    def test_deleteTask_statusCheck(self):
        response = self.client.delete('/api/task/2')
        self.assertEqual(response.status_code, 204)

    def test_deleteTask_authorization(self):
        new_user = User.objects.create_user("newuser", "new@user.com", "newpass")
        new_token = Token.objects.create(user=new_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + new_token.key)
        response = self.client.delete('/api/task/2')
        self.assertEqual(response.status_code, 403)

    def test_updateTaskStatus_authorization(self):
        new_user = User.objects.create_user("newuser", "new@user.com", "newpass")
        new_token = Token.objects.create(user=new_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + new_token.key)
        body_data = {'status':1}
        task_data =urllib.parse.urlencode(body_data) 
        response = self.client.patch('/api/task/2', data=task_data,content_type='application/x-www-form-urlencoded')
        self.assertEqual(response.status_code, 403)

    

class CategoryTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        self.token = Token.objects.create(user=self.user)
        self.client.force_login(user=self.user)

    def test_createNewCategory(self):
        body_data = {'name':"new_category_1"}
        category_data =urllib.parse.urlencode(body_data) 
        response = self.client.post('/api/category', data=category_data,content_type='application/x-www-form-urlencoded')
        self.assertEqual(response.status_code, 201)

    def test_getAllCatgories(self):
        body_data = {'name':"new_category_1"}
        category_data =urllib.parse.urlencode(body_data) 
        self.client.post('/api/category', data=category_data,content_type='application/x-www-form-urlencoded')
        response = self.client.get('/api/category')
        self.assertEqual(len(response.data), 1)


class SearchTasksTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('admin', 'admin@admin.com', 'admin123')
        self.token = Token.objects.create(user=self.user)
        self.client.force_login(user=self.user)

        category_1 = Category.objects.create(
            name='category1',user_id=self.user.id, id= 1
        )

        Task.objects.create(
            title='task1',description='task1 description',user_id=self.user.id,category=category_1,due_date=now() + timedelta(days=7)
        )

        Task.objects.create(
            title='task2',description='task2 description',user_id=self.user.id,category=category_1,due_date=now() + timedelta(days=7)
        )

        Task.objects.create(
            title='task3',description='unique word cheese',user_id=self.user.id,category=category_1,due_date=now() + timedelta(days=7),status = 1
        )

    def test_checkResponse(self):
        response = self.client.get('/api/search?search=task')
        self.assertEqual(response.status_code, 200)

    def test_searchTitle(self):
        response = self.client.get('/api/search?search=task')
        self.assertEqual(len(response.data), 3)

    def test_searchDescription(self):
        response = self.client.get('/api/search?search=cheese')
        self.assertEqual(len(response.data), 1)







