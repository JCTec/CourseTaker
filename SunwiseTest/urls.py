"""SunwiseTest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import include, path
from course import urls as course_urls
from question import urls as question_urls
from student import urls as student_urls
from users.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', login),

    path('api/course/', include(course_urls.urlpatterns)),
    path('api/', include(question_urls.urlpatterns)),
    path('api/student/', include(student_urls.urlpatterns))
]
