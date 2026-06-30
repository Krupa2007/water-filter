"""
URL configuration for filter project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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

from django.urls import path
from filapp.views import *
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path



urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_page ,name='login'),
    path('register/',register, name='register'),
    path('forgot/', forgot ,name='forgot'),
    path('dashboard/', dashboard ,name='dashboard'),
    path('home/', home ,name='home'),
    path('main/', main ,name='main'),
    path('qrcode/', qr ,name='qrcode'),
    path('water_quality/',water_quality ,name='water_quality'),
    path('delete-pet/<id>/', delete_pet ,name='delete_pet'),
    path('add/', add ,name='add_profile'),
    path('update/<int:id>/', update_data ,name='update_profile'),
     path('analytics/', analytics_view, name='analytics'),
      path('export/', export_page, name='export_pdf'),
      path('profile/', profile, name='profile'),
      path('model/', model, name='model'),
    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root = settings.MEDIA_ROOT )

urlpatterns += staticfiles_urlpatterns()  