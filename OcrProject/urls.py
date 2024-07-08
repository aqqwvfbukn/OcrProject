"""
URL configuration for OcrProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path,re_path
from django.views.static import serve
from django.conf import settings

from ocr import views

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root':settings.MEDIA_ROOT}, name ='media'),

    path('admin/', admin.site.urls),

    path('base/', views.base),

    path('ocr/', views.ocr),

    # 登录
    path('login/', views.login),
    path('login_code/', views.login_code),
    path('logout/', views.logout),
    path('send_message/', views.send_message),



]
