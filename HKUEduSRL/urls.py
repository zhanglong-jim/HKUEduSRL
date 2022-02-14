"""HKUEduSRL URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from HKUEduSRLApp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.login),
    path('login/',views.login),
    path('index/',views.index),
    path('jsmind/',views.jsmind),
    path('add/', views.record_add),
    path('logout/',views.logout),
    path('mysrl/',views.mysrl),
    path('new/',views.new),
    path('ft/',views.ft),
    path('Goal/',views.Goal),
    path('Env/',views.Env),
    path('Task/',views.Task),
    path('Time/',views.Time),
    path('Help/',views.Help),
    path('Sel/',views.Sel)
]
