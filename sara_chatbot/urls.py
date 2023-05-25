"""sara_chatbot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

from django.urls import path ,include
from django.contrib.auth.views import LogoutView,LoginView
from sara_app.views import chatbot, add_events, main, admin, add_teachers,event_dashboard,employees_dashboard,show_employees



urlpatterns = [
    # path("admin/", admin.site.urls),
    path('login', LoginView.as_view(template_name='login1.html'),name='login'),
    path('logout', LogoutView.as_view(template_name='main.html'),name='logout'),
    path('chatbot/', chatbot, name='chatbot'),
    path('admin/', admin, name='admin'),
    path('', main , name='main'),
    path('add_teachers/', add_teachers, name='add_teachers' ),
    path('add_events/', add_events, name='add_events'),
    path('event_dashboard/', event_dashboard, name='event_dashboard'),
    path('employees_dashboard/', employees_dashboard, name='employees_dashboard'),
    path('show_employees/',show_employees , name='show_employees'),

    
]
