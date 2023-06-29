from django.urls import path
from .views import *

urlpatterns = [
    path(r"create_system/", CreateElevatorSystemView.as_view(), name="create_elevator_system")
]