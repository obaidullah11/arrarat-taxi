from rest_framework import serializers
from .models import *


class AssignPassengerTosignaturesheet1Serializer(serializers.ModelSerializer):
    # Add the passenger name field to the serializer
    passenger_name = serializers.ReadOnlyField(source='passenger.name')

    class Meta:
        model = AssignPassengerTosignature_sheet1
        fields = ['id', 'user', 'passenger', 'date_created', 'passenger_name']





from rest_framework import serializers
from .models import SignatureReceipt

class CreateSignatureReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignatureReceipt
        fields = (

            'Driver',
            'account_name',
            'start_time',
            'finish_time',
            'trip_explanation',
            'start_point',
            'drop_point',
            'taxi_no',
            'dc_no',
            'passenger_name',
            'fare_meter',
            'extras',
            'total',
            'signature'

        )



class SignatureReceiptimageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignatureReceipt
        fields = '__all__'  # Include all fields, including the 'signature' field
