from django.urls import path
from . import views

urlpatterns = [
    path('', views.NewsListView.as_view(), name='news-list'),
    path('<int:pk>/', views.NewsDetailView.as_view(), name='news-detail'),
    path('add/', views.NewsCreateView.as_view(), name='news-add'),
]
