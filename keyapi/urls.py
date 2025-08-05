from django.urls import path
from .views import GetKey

urlpatterns = [
    path('key/', GetKey.as_view(), name='get_key'),
]