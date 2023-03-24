from django.urls import path
from .views import *

urlpatterns = [
    path('<str:key>', StartView.as_view(), name='start')
]