from django.urls import path
from . import views

app_name = 'orc'

urlpatterns = [
    path('index', views.IndexView.as_view(), name = 'index'),
    path('post_list', views.PostListView.as_view(), name = 'post_list'),
    path('post_form', views.PostCreateFormView.as_view(), name='post_form'),
    path('post_detail/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'), 
    path('post_update/<int:pk>/', views.PostUpdateView.as_view(), name='post_update'), 
    path('post_delete/<int:pk>/', views.PostDeleteView.as_view(), name='post_delete'), 
    path('post_bulk_delete', views.PostBulkDeleteView.as_view(), name = 'post_bulk_delete'),
]