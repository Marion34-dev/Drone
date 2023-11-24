from django.urls import path
from .views import ReceiveDataView, LocationView

urlpatterns = [
    path('receive_data/', ReceiveDataView.as_view(), name='receive_data'),
    path('map/', LocationView.as_view(), name='map'),
]