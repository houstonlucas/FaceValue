from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import logout_view
from .forms import CustomAuthenticationForm

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html',
        authentication_form=CustomAuthenticationForm
    ), name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/<int:pk>/promote/', views.promote_to_admin, name='promote_to_admin'),
    path('users/<int:pk>/demote/', views.demote_from_admin, name='demote_from_admin'),
    path('users/<int:pk>/delete/', views.delete_user, name='delete_user'),
]
