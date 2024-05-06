from django.urls import path, include 
from auth_.views import Register
from rest_framework import routers

# from .views import UserViewSet

#маршрутизаторы
router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', Register.as_view(), name='register'),
]

urlpatterns += router.urls