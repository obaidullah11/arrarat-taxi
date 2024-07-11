from django.shortcuts import render
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
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
# Create your views here.





@api_view(['POST'])
def create_signature_receipt(request):
    if request.method == 'POST':
        serializer = CreateSignatureReceiptSerializer(data=request.data)
        try:
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
            else:
                errors = serializer.errors
                # Print validation errors
                print(errors)
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Handle any other exceptions that may occur during the creation process
            print(f"An error occurred: {str(e)}")
            return Response({'message': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
    queryset = dockets.objects.all()
    serializer_class = SignatureReceiptimageSerializer




# class SignatureReceiptListView(generics.ListAPIView):
#     serializer_class = SignatureReceiptimageSerializer

#     def get_queryset(self):
#         driver_id = self.kwargs['driver_id']  # Get the driver_id from the URL parameter

#         # Calculate the sum of 'total' field for all records for the driver
#         total_sum = dockets.objects.filter(Driver_id=driver_id).aggregate(total_sum=Sum('total'))['total_sum'] or 0

#         # Count the number of passengers for the driver
#         passenger_count = dockets.objects.filter(Driver_id=driver_id).values('passenger_name').distinct().count()

#         # Retrieve the queryset of records for the driver
#         queryset = dockets.objects.filter(Driver_id=driver_id)

#         return queryset  # Return the queryset, don't return Response here

#     def list(self, request, *args, **kwargs):
#         # Call the parent class's list method to get the serialized data
#         queryset = self.get_queryset()
#         serializer = self.serializer_class(queryset, many=True)
#         total_sum = queryset.aggregate(total_sum=Sum('total'))['total_sum'] or 0

#         # Count the number of passengers for the driver
#         passenger_count = queryset.values('passenger_name').distinct().count()


#         # Create the response data
#         response_data = {
#             'dockets_total_sum': total_sum,
#             'dockets_passenger_count': passenger_count,
#             'results': serializer.data,
#         }

#         return Response(response_data)





class SignatureReceiptListView(generics.ListAPIView):
    serializer_class = SignatureReceiptimageSerializer

    def get_queryset(self):
        driver_id = self.kwargs['driver_id']  # Get the driver_id from the URL parameter

        try:
            today = timezone.now().date()
            start_of_week = today - timedelta(days=today.weekday())
            end_of_week = start_of_week + timedelta(days=6)

            # Calculate the sum of 'total' field for all records for the driver within the current week
            total_sum = (
                dockets.objects
                .filter(Driver_id=driver_id, date__date__range=[start_of_week, end_of_week])
                .aggregate(total_sum=Sum('total'))['total_sum'] or Decimal('0.00')
            )

            # Count the number of distinct passengers for the driver within the current week
            passenger_count = (
                dockets.objects
                .filter(Driver_id=driver_id, date__date__range=[start_of_week, end_of_week])
                .values('passenger_name').distinct().count()
            )

            # Retrieve the queryset of records for the driver within the current week
            queryset = (
                dockets.objects
                .filter(Driver_id=driver_id, date__date__range=[start_of_week, end_of_week])
            )

            return queryset  # Return the queryset, don't return Response here

        except Exception as e:
            return dockets.objects.none()  # Return an empty queryset in case of an exception

    def list(self, request, *args, **kwargs):
        # Call the parent class's list method to get the serialized data
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)

        # Calculate the total sum and passenger count based on the filtered queryset
        total_sum = queryset.aggregate(total_sum=Sum('total'))['total_sum'] or Decimal('0.00')
        passenger_count = queryset.values('passenger_name').distinct().count()

        # Create the response data
        response_data = {
            'dockets_total_sum': total_sum,
            'dockets_passenger_count': passenger_count,
            'results': serializer.data,
        }

        return Response(response_data)