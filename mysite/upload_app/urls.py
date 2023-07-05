from django.urls import path
from . import views

app_name = 'upload_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('preview/<int:image_id>/', views.preview, name='preview'),
]