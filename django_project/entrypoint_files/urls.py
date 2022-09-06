from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from django.http import HttpResponse


urlpatterns = [
    path('admin/', admin.site.urls),
    path('lm/', include("lm_app.urls")),
    path('', lambda request: redirect('lm/api/docs'), name = "index"),
]
