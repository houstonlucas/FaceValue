from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import logout_view

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('users/', views.UserListView.as_view(), name='user_list'),
]
