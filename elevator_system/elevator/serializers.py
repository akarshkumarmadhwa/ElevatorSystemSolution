from rest_framework import serializers

from elevator.models import ElevatorSystem

class CreateElevatorSystemSerializer(serializers.ModelSerializer):
  '''
  Model serializer for model ElevatorSystem
  '''
  class Meta:
    model = ElevatorSystem
    fields = '__all__'