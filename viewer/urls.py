from django.urls import path
from viewer.views import *

urlpatterns = [
    path('', show_passes, name='show_passes')
]