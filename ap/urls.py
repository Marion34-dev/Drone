from django.urls import path
from .views import ReceiveDataView

urlpatterns = [
    path('receive_data/', ReceiveDataView.as_view(), name='receive_data'),
 ]