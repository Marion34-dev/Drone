from django.urls import path
from .views import ReceiveDataView

urlpatterns = [
    path('tracker/', ReceiveDataView.as_view(), name='tracker'),
]