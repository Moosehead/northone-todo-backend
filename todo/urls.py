# api/urls.py
# api/urls.py
from django.urls import include, path

from . import views

urlpatterns = [
	path('task', views.TaskView.as_view(), name="get_matches"),
	path('task/<str:pk>', views.TaskDetailView.as_view(), name="task-update"),
	path('search', views.search_tasks, name="get_matches"),
	path('category', views.CategoryView.as_view(), name="get_matches"),
	path('auth/', include('rest_auth.urls')),
	path('auth/registration/', include('rest_auth.registration.urls')),
]
