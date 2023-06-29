import json
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from elevator.serializers import CreateElevatorSystemSerializer

class CreateElevatorSystemView(APIView):
    http_method_names = ["get", "post"]

    def post(self, request):
        try:
            data = json.dumps(request.data)
            print(data)
            serializer = CreateElevatorSystemSerializer(data=request.data, context={"request": request})
            if serializer.is_valid():
                elevator_system = serializer.save()
                return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
