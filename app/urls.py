from django.urls import path

from . import views
from .token import WEBHOOK_ENDPOINT

urlpatterns = [
    path(f'{WEBHOOK_ENDPOINT}/', views.IndexView.as_view(), name='index'),
]
