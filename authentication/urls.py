from django.urls import path
from .views import *


urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard' ),
    path('login/', custom_login, name='login'),
    path('logout/', custom_logout, name='logout'),
]