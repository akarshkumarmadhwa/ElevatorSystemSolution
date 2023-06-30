from django.urls import path
from .views import *

urlpatterns = [
    #For creating elevator system and initialize with N elevators and also to list the systems
    path(r"elevator_system/", ElevatorSystemView.as_view(), name="create_elevator_system"),

    #For listing elevators of a system and to open/close door along with marking as operational/maintainaince
    path(r"", ElevatorView.as_view(), name="elevator"),

    #Adding user request to maintain the record for each request associated with elevator
    path(r"ele_sys_req/", CreateElevatorRequest.as_view(), name="elevator_request"),

    #Fetch the details of elevator destination, moving up/down, running ,operational
    path(r"destination", FetchElevatorDestination.as_view(), name="elevator_destination"),
]