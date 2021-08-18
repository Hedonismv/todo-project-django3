"""todowoo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from todo import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth
    path('signup/', views.signupUser, name="signupUser"),
    path('logout/', views.logoutUser, name="logoutUser"),
    path('login/', views.loginUser, name="loginUser"),
    #Todos
    path('current/', views.currentTodos, name="currentTodos"),
    path('completed/', views.completedTodos, name="completedTodos"),
    path('create/', views.createTodos, name="createTodos"),
    path('todo/<int:todo_pk>/', views.viewTodos, name="viewTodos"),
    path('todo/<int:todo_pk>/complete', views.completeTodos, name="completeTodos"),
    path('todo/<int:todo_pk>/delete', views.deleteTodos, name="deleteTodos"),
    path('', views.home, name="home")
]
