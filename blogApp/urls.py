from django.urls import path
from . import views
from .views import (
    PostListView, 
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView
)

urlpatterns = [
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('', PostListView.as_view(), name='blogApp-home'),  
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),   
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'), 
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),  
    path('about/', views.about, name='blogApp-about'),
    path('logout/', views.logout_view, name='blogApp-logout'),
]
