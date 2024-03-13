"""
URL configuration for resaclinic project.

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
from django.conf.urls.static import static
from django.urls import include, path
from resaclinic import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',  include(('clinic.urls', 'clinic'), namespace='clinic')),
    path('resa/', include('centric.urls')),
    path('reception/', include('resaclinic.receptionist_urls')),
    path('doctor/', include('resaclinic.doctor_urls')),
    path('nurse/', include('resaclinic.nurse_urls')),
    path('accounts/', include('django.contrib.auth.urls')), 
    path('kahama/', include(('kahamahmis.urls', 'kahamahmis'), namespace='kahamahmis')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_URL)