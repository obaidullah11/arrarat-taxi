from rest_framework import serializers
from .models import *

class PassengerSerializer(serializers.ModelSerializer):
     class Meta:
        model = Passenger
        fields = '__all__'
class ShiftTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShiftTime
        fields = '__all__'

# class Runsheet1Serializer(serializers.ModelSerializer):
#     class Meta:
#         model = Runsheet1
#         fields = '__all__'




class Runsheet1Serializer(serializers.ModelSerializer):
    passenger_name_name = serializers.CharField(source='passenger_name.name', read_only=True)

    class Meta:
        model = Runsheet1
        fields = ['id', 'passenger_name', 'passenger_name_name', 'Morning_price', 'Evening_price', 'driver', 'date_created']
# serializers.py


class Runsheet1BulkUpdateSerializer(serializers.ModelSerializer):
      class Meta:
        model = Runsheet1
        fields = '__all__'
############################require for all
class AssignPassengerToRunsheet1Serializer(serializers.ModelSerializer):
    # Add the passenger name field to the serializer
    passenger_name = serializers.ReadOnlyField(source='passenger.name')

    class Meta:
        model = AssignPassengerToRunsheet1
        fields = ['id', 'user', 'passenger', 'date_created', 'passenger_name']

class AssignPassengerToRunsheet2Serializer(serializers.ModelSerializer):
    # Add the passenger name field to the serializer
    passenger_name = serializers.ReadOnlyField(source='passenger.name')

    class Meta:
        model = AssignPassengerToRunsheet2
        fields = ['id', 'user', 'passenger', 'date_created', 'passenger_name']
class AssignPassengerToRunsheet3Serializer(serializers.ModelSerializer):
    # Add the passenger name field to the serializer
    passenger_name = serializers.ReadOnlyField(source='passenger.name')

    class Meta:
        model = AssignPassengerToRunsheet3
        fields = ['id', 'user', 'passenger', 'date_created', 'passenger_name']
class AssignPassengerToRunsheet4Serializer(serializers.ModelSerializer):
    # Add the passenger name field to the serializer
    passenger_name = serializers.ReadOnlyField(source='passenger.name')

    class Meta:
        model = AssignPassengerToRunsheet4
        fields = ['id', 'user', 'passenger', 'date_created', 'passenger_name']
class AssignPassengerToRunsheet5Serializer(serializers.ModelSerializer):
    # Add the passenger name field to the serializer
    passenger_name = serializers.ReadOnlyField(source='passenger.name')

    class Meta:
        model = AssignPassengerToRunsheet5
        fields = ['id', 'user', 'passenger', 'date_created', 'passenger_name']
class AssignPassengerToRunsheet6Serializer(serializers.ModelSerializer):
    # Add the passenger name field to the serializer
    passenger_name = serializers.ReadOnlyField(source='passenger.name')

    class Meta:
        model = AssignPassengerToRunsheet6
        fields = ['id', 'user', 'passenger', 'date_created', 'passenger_name']
class AssignPassengerToRunsheet7Serializer(serializers.ModelSerializer):
    # Add the passenger name field to the serializer
    passenger_name = serializers.ReadOnlyField(source='passenger.name')

    class Meta:
        model = AssignPassengerToRunsheet7
        fields = ['id', 'user', 'passenger', 'date_created', 'passenger_name']
class AssignPassengerToRunsheet8Serializer(serializers.ModelSerializer):
    # Add the passenger name field to the serializer
    passenger_name = serializers.ReadOnlyField(source='passenger.name')

    class Meta:
        model = AssignPassengerToRunsheet8
        fields = ['id', 'user', 'passenger', 'date_created', 'passenger_name']
##########################################

class Runsheet1Serializer(serializers.ModelSerializer):
    class Meta:
        model = Runsheet1
        fields = '__all__'



class Runsheet2Serializer(serializers.ModelSerializer):
    class Meta:
        model = Runsheet2
        fields = '__all__'


class Runsheet3Serializer(serializers.ModelSerializer):
    class Meta:
        model = Runsheet3
        fields = '__all__'

class Runsheet4Serializer(serializers.ModelSerializer):
    class Meta:
        model = Runsheet4
        fields = '__all__'



class Runsheet5Serializer(serializers.ModelSerializer):
    class Meta:
        model = Runsheet5
        fields = '__all__'

class Runsheet6Serializer(serializers.ModelSerializer):
    class Meta:
        model = Runsheet6
        fields = '__all__'



class Runsheet7Serializer(serializers.ModelSerializer):
    class Meta:
        model = Runsheet7
        fields = '__all__'



class Runsheet8Serializer(serializers.ModelSerializer):
    class Meta:
        model = Runsheet8
        fields = '__all__'


class RunsheetSumSerializer(serializers.Serializer):
    morning_sum = serializers.DecimalField(max_digits=8, decimal_places=2)
    evening_sum = serializers.DecimalField(max_digits=8, decimal_places=2)
    passenger_count = serializers.IntegerField()
    passengers = serializers.ListField(child=PassengerSerializer())  # Create PassengerSerializer for passenger details













































class HelpAndDisputeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpAndDispute
        fields = '__all__'