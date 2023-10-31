from django.urls import path 
from .views import *

urlpatterns = [path('chat', testview.as_view(),name="main"),
]   