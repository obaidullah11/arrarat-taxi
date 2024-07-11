from django.shortcuts import render
from django.db.models import Sum
from django.db.models.functions import TruncDate
from rest_framework import status
from django.conf import settings
from datetime import date
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.generics import ListAPIView, UpdateAPIView
from .serializers import *

# Create your views here.
class AssignPassengerByDriversignaturesheetAPIView(ListAPIView):
    serializer_class = AssignPassengerTosignaturesheet1Serializer

    def get_queryset(self):
        # Get the driver_id from the URL parameter
        driver_id = self.kwargs['driver_id']

        # Filter the queryset to retrieve passenger assignments for the given driver_id
        queryset = AssignPassengerTosignature_sheet1.objects.filter(user_id=driver_id)

        return queryset
    




@api_view(['POST'])
def add_signature_sheet(request):
    if request.method == 'POST':
        # Get the current date and time
        current_datetime = timezone.now()
        
        # Check if a record already exists for the current date
        existing_record = signature_sheet1.objects.filter(date_created__date=current_datetime.date()).first()

        if existing_record:
            message = "A record for today already exists."
            return Response({"message": message}, status=status.HTTP_201_CREATED)

        serializer = SignatureSheetSerializer(data=request.data)

        if serializer.is_valid():
            # Set the date_created field to the current date and time before saving
            serializer.save(date_created=current_datetime)
            message = "Record created successfully."
            return Response({"message": message, "data": serializer.data}, status=status.HTTP_201_CREATED)
        
        errors = serializer.errors
        return Response({"errors": errors}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_driver_records1(request, driver_id):
    runsheets = signature_sheet1.objects.filter(driver__id=driver_id)

    if not runsheets.exists():
        return Response({'message': 'No data found for the specified driver.'}, status=status.HTTP_200_OK)

    if not runsheets.exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    print(f"Driver ID: {driver_id}")
    print(f"Number of run sheets found: {runsheets.count()}")
    runsheets = runsheets.annotate(date=TruncDate('date_created')).order_by('date')
    runsheet_array = []
    total_morning_all = 0
    total_evening_all = 0
    grouped_runsheets = {}

    for runsheet in runsheets:
        date = runsheet.date
        formatted_date = date.strftime("%A %d/%m/%Y")
        passenger_name = runsheet.passenger_name.name  # Assuming name is a field in the Passenger model
        driver_name = runsheet.driver.name  # Assuming name is a field in the User model

        # Generate the URL for the signature image
        signature_url = settings.MEDIA_URL + str(runsheet.signature)

        runsheet_data = {
            'id': runsheet.id,  # Include the runsheet ID
            'passenger_name': passenger_name,
            'formatted_date_created': formatted_date,
            'Morning_price': runsheet.Morning_price,
            'Evening_price': runsheet.Evening_price,
            'driver': driver_name,
            'signature': request.build_absolute_uri(signature_url),  # Include the signature URL
        }

        if formatted_date in grouped_runsheets:
            grouped_runsheets[formatted_date]['runsheets'].append(runsheet_data)
            grouped_runsheets[formatted_date]['total_morning_price'] += runsheet.Morning_price if runsheet.Morning_price is not None else 0
            grouped_runsheets[formatted_date]['total_evening_price'] += runsheet.Evening_price if runsheet.Evening_price is not None else 0
        else:
            grouped_runsheets[formatted_date] = {
                'formatted_date_created': formatted_date,
                'runsheets': [runsheet_data],
                'total_morning_price': runsheet.Morning_price if runsheet.Morning_price is not None else 0,
                'total_evening_price': runsheet.Evening_price if runsheet.Evening_price is not None else 0,
            }

        total_morning_all += runsheet.Morning_price if runsheet.Morning_price is not None else 0
        total_evening_all += runsheet.Evening_price if runsheet.Evening_price is not None else 0

    for date_key in grouped_runsheets:
        runsheet_array.append(grouped_runsheets[date_key])

    # Add overall totals to the response data
    response_data = {
        'grouped_runsheets': runsheet_array,
        'total_morning_all': total_morning_all,
        'total_evening_all': total_evening_all,
    }

    return Response(response_data)






@api_view(['POST'])
def create_signature_receipt(request):
    if request.method == 'POST':
        serializer = CreateSignatureReceiptSerializer(data=request.data)
        if serializer.is_valid():
            # Save the serialized data to create a new record
            instance = serializer.save()
            # Retrieve the ID of the created record
            created_id = instance.id
            # Include a custom message and the ID in the response data
            response_data = {
                'message': 'SignatureReceipt record created successfully',
                'id': created_id,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_signature_image_receipt(request):
    if request.method == 'POST':
        serializer = SignatureReceiptimageSerializer(data=request.data)
        if serializer.is_valid():
            # Save the serialized data to create a new record
            instance = serializer.save()

            # Check if 'signature' file was included in the request
            signature_file = request.data.get('signature', None)
            if signature_file:
                # If the 'signature' file is provided, associate it with the record
                instance.signature = signature_file
                instance.save()

            # Retrieve the ID of the created record
            created_id = instance.id

            # Include a custom message and the ID in the response data
            response_data = {
                'message': 'SignatureReceipt record created successfully',
                'id': created_id,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class SignatureReceiptListCreateView(generics.ListCreateAPIView):
    queryset = SignatureReceipt.objects.all()
    serializer_class = SignatureReceiptimageSerializer