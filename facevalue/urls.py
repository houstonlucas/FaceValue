"""
URL configuration for facevalue project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import (
    home,
    PuzzleManagementView,
    PuzzleCreateView,
    PuzzleUpdateView,
    PuzzleDeleteView,
    PuzzleDetailView,
    ReviewCreateView,
    ReviewUpdateView,
    ReviewDeleteView,
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView,
    ReviewListView,
    AdminDashboardView,
    healthz,  # health-check endpoint
)

urlpatterns = [
    path('', home, name='home'),
    path('healthz/', healthz, name='healthz'),
    path('admin/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('admin/django/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('puzzles/', PuzzleManagementView.as_view(), name='puzzle_management'),
    path('puzzles/add/', PuzzleCreateView.as_view(), name='puzzle_create'),
    path('puzzles/<int:pk>/edit/', PuzzleUpdateView.as_view(), name='puzzle_update'),
    path('puzzles/<int:pk>/delete/', PuzzleDeleteView.as_view(), name='puzzle_delete'),
    # Puzzle detail & review/comment actions
    path('puzzles/<slug:slug>/', PuzzleDetailView.as_view(), name='puzzle_detail'),
    path('puzzles/<slug:slug>/review/add/', ReviewCreateView.as_view(), name='review_add'),
    path('review/<int:pk>/edit/', ReviewUpdateView.as_view(), name='review_update'),
    path('review/<int:pk>/delete/', ReviewDeleteView.as_view(), name='review_delete'),
    path('review/<int:review_pk>/comment/add/', CommentCreateView.as_view(), name='comment_add'),
    path('comment/<int:pk>/edit/', CommentUpdateView.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
    # Reviews list page
    path('reviews/', ReviewListView.as_view(), name='review_list'),
    path('reviews/add/', ReviewCreateView.as_view(), name='review_create'),
]
