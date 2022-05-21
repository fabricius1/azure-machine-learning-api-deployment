from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

urlpatterns = [
    path('admin/', admin.site.urls),
    path('lm/', include("lm_app.urls")),
    path('', lambda request: HttpResponse("<h1>Index page</h1>"), name = "index"),
]
