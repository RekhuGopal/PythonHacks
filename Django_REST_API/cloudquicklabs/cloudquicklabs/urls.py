"""
URL configuration for cloudquicklabs project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path , include ,re_path
from users import views
app_name = 'users'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('cars.urls')),
    re_path('api/register-by-access-token/' + r'social/(?P<backend>[^/]+)/$', views.register_by_access_token),
    path('api/authentication-test/', views.authentication_test)
]
