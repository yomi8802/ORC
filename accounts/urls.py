from django.urls import path
from . import views

app_name ='accounts'

urlpatterns =[
    path('signup/', views.MySignupView.as_view(), name='signup'),
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('logout/', views.MyLogoutView.as_view(), name='logout'),
    path('user/', views.MyUserView.as_view(), name='user'),
]