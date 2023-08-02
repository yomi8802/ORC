from django.urls import path
from . import views

app_name = 'orc'

urlpatterns = [
    path('index', views.IndexView.as_view(), name = 'index'),
    path('post_list', views.PostListView.as_view(), name = 'post_list'),
    path('post_form', views.PostCreateFormView.as_view(), name='post_form'),
    path('post_detail/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'), 
]