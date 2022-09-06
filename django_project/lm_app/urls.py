from django.urls import path
from . import views
from .api import api


urlpatterns = [
    path('', views.main, name="main"),
    # path('predict/<int:distance>/', views.predict, name="predict"),
    path('api/', api.urls),
]