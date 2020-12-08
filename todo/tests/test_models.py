from django.test import TestCase
from datetime import datetime, timedelta,date
from django.utils.timezone import now
from ..models import Task,Category

class CategoryTest(TestCase):
    """ Test module for Category model """

    def setUp(self):
        Category.objects.create(
            name='category1',user_id='1'
        )
        Category.objects.create(
            name='category2',user_id='1' 
        )

    def test_category_creation(self):
        category1 = Category.objects.get(name='category1')
        category2 = Category.objects.get(name='category2')
        self.assertEqual(
            category1.name, "category1")
        self.assertEqual(
            category1.user_id,'1')
        self.assertEqual(
            category2.name, "category2")
        self.assertEqual(
            category2.user_id, '1')


class TaskTest(TestCase):
    """ Test module for Task model """
    def setUp(self):
        Category.objects.create(
            name='category1',user_id='1'
        )
        category_1 = Category.objects.get(name='category1')

        Task.objects.create(
            title='task2',description='task2 description',user_id='1',category=category_1,due_date=now() + timedelta(days=7)
        )

    def test_category_creation(self):
        task2 = Task.objects.get(title='task2')
        self.assertEqual(
            task2.title, 'task2')
        self.assertEqual(
            task2.category_name, 'category1')

