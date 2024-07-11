



from rest_framework import serializers
from .models import dockets

class CreateSignatureReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = dockets
        fields = (
            # 'date',
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
        model = dockets
        fields = '__all__'  # Include all fields, including the 'signature' field
