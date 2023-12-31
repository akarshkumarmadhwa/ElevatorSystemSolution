from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from elevator.models import Elevator, ElevatorRequest, ElevatorSystem

from elevator.serializers import ElevatorRequestSerializer, ElevatorRequestSerializerAll, ElevatorSystemSerializer, ElevatorSerializer
from elevator.utils import create_elevators


class ElevatorSystemView(APIView):
    """
    This api is for listing the elevator systems as well as for creating one along with initializing the elevators 
    with provided number of elevator as post data.
    """
    http_method_names = ["get", "post"]

    def get(self, request):
        try:
            elev_sys_id = request.query_params.get("elev_sys_id", None)
            if elev_sys_id:
                elev_sys_id = elev_sys_id.split(",")
                query_set = ElevatorSystem.objects.filter(id__in=elev_sys_id)
            else:
                query_set = ElevatorSystem.objects.all()
            serializer = ElevatorSystemSerializer(query_set, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)

    def post(self, request):
        try:
            serializer = ElevatorSystemSerializer(data=request.data, context={"request": request})
            if serializer.is_valid():
                elevator_system = serializer.save()
                create_elevators(
                    number_of_elevators=elevator_system.number_of_elevators,
                    system_id=elevator_system.id
                    )
                return Response(status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)

class ElevatorView(APIView):
    """
    Given an elevator system list the elevators and their status along with to update the elevator. 
    """
    http_method_names = ["get", "put"]

    def get(self, request):
        try:
            sys_id = request.query_params.get("sys_id", None)
            elev_num = request.query_params.get("elev_num", None)
            if not sys_id:
                return Response(data={"ElevatorSystem ID sys_id is required!"}, status=status.HTTP_400_BAD_REQUEST)
            if elev_num:
                elev_num = elev_num.split(",")
                query_set = Elevator.objects.filter(elevator_number__in=elev_num, elevator_system__id=sys_id)
            else:
                query_set = Elevator.objects.filter(elevator_system__id=sys_id)
            serializer = ElevatorSerializer(query_set, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)

    def put(self, request):
        try:
            sys_id = request.query_params.get("sys_id", None)
            elev_num = request.query_params.get("elev_num", None)
            data = request.data
            data["elevator_number"] = elev_num
            if not sys_id:
                return Response(data={"ElevatorSystem ID sys_id is required!"}, status=status.HTTP_400_BAD_REQUEST)
            if not elev_num:
                return Response(data={"Elevator number elev_num is required and to be passed in url header!"}, status=status.HTTP_400_BAD_REQUEST)
            query_set = Elevator.objects.get(elevator_number=elev_num, elevator_system__id=sys_id)
            serializer = ElevatorSerializer(query_set, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_202_ACCEPTED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)

class CreateElevatorRequest(APIView):
  """
  Create a new request for a specific elevator, 
  given its elevator system and elevator number with URL.
  The inputs of requested and destinatiom floor is sent with
  the form-data.
  """

  def get(self, request):
    sys_id = request.query_params.get("sys_id", None)
    elev_num = request.query_params.get("elev_num", None)

    elevator_objects = Elevator.objects.filter(
      elevator_system__id = sys_id,
      elevator_number = elev_num
    ).order_by("id")

    if elevator_objects:
       elevator_object = elevator_objects.first()

    queryset = ElevatorRequest.objects.filter(elevator=elevator_object)
    serializer = ElevatorRequestSerializerAll(queryset, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)

  def post(self, request):
    try:
        sys_id = request.query_params.get("sys_id", None)
        elev_num = request.query_params.get("elev_num", None)
        queryset = Elevator.objects.filter(
        elevator_system__id = sys_id,
        elevator_number = elev_num
    ).order_by("id").first()
        serializer = ElevatorRequestSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            elevator_system_req = serializer.save()
            elevator_system_req.elevator = queryset
            elevator_system_req.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)

class FetchElevatorDestination(APIView):
  """
  Fetch the next destination floor for a given elevator
  along with status moving up/down
  """
  def get(self, request):
    elevator_object = None
    sys_id = request.query_params.get("sys_id", None)
    elev_num = request.query_params.get("elev_num", None)

    elevator_objects = Elevator.objects.filter(
      elevator_system__id = sys_id,
      elevator_number = elev_num
    ).order_by("id")

    if elevator_objects:
      elevator_object = elevator_objects.first()

    requests_pendings = ElevatorRequest.objects.filter(
      elevator = elevator_object,
      is_active = True,
    ).order_by("request_time")

    if requests_pendings:
       requests_pending = requests_pendings.first()

    return_dict = {

    }

    if not elevator_object:
      return_dict = {
        "moving_up": None,
        "moving_down": None, 
        "running" : None,
        "destination_floor" : None,
        "comment": "The Elevator number or elevator system id is incorrect or missing!"
      }
      
    elif not elevator_object.is_operational:
      return_dict = {
        "moving_up": None,
        "moving_down": None,   
        "running" : False,
        "destination_floor" : None,
        "comment": "The Elevator is not operational!"
      }
    elif not requests_pendings:
      return_dict = {
        "moving_up": None,
        "moving_down": None,   
        "running" : False,
        "destination_floor" : None,
        "comment": "The Elevator is not running currently, No pending requests!"
      }
    elif requests_pending.requested_floor == elevator_object.current_floor:
      return_dict = {
        "moving_up": False,
        "moving_down": False, 
        "running" : False,
        "destination_floor" : str(requests_pending.destination_floor),
        "comment": None
      }
    elif requests_pending.requested_floor > elevator_object.current_floor:
        return_dict = {
            "moving_up": True,
            "moving_down": False,     
            "running" : True,
            "destination_floor" : str(requests_pending.requested_floor),
            "comment": None
        }
    else:
        return_dict = {
            "moving_up": False,
            "moving_down": True,           
            "running" : True,
            "destination_floor" : str(requests_pending.requested_floor),
            "comment": None
        }


    return Response(return_dict)