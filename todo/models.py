from django.db import models
import django.db.models.fields as fields
from django.utils import timezone


# Create your models here.

class Category(models.Model):
    """
    This model stores the odds from all books for all events that
    are happening today in JSON format so that it can be consumed
    by the frontend
    """
    name = fields.CharField(max_length = 250)
    user_id = fields.CharField(max_length=256)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "category"
        verbose_name = "list of categories for the user"

class Task(models.Model):
    """
    This model stores the odds from all books for all events that
    are happening today in JSON format so that it can be consumed
    by the frontend
    """
    title = fields.CharField(max_length = 500)
    description = fields.TextField(max_length = 1000)
    status = fields.PositiveIntegerField(default=0)
    user_id = fields.CharField(max_length=256)
    timestamp = fields.DateTimeField(auto_now = True)
    due_date = fields.DateTimeField(null=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE, null=True,blank=True)
    
    def __str__(self):
        return self.title

    @property
    def category_name(self):
        return self.category.name

    class Meta:
        db_table = "task"
        verbose_name = "list of tasks for users"

