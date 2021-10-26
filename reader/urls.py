from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),

    path('create-article/', views.createArticle, name='create-article'),

    path('topic/<str:category>', views.topicPage, name='topic-page'),
    path('news/<str:pk>', views.newsArticle, name='news-article')
]
