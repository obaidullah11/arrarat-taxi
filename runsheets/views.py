from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from django.http import JsonResponse
from datetime import timedelta
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.utils.decorators import method_decorator
from django.db.models import Sum
from decimal import Decimal
from .serializers import *
from .models import *
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import ListAPIView, UpdateAPIView
from django.db.models import Sum
from django.db.models.functions import TruncDate
import json

import logging
logger = logging.getLogger(__name__)


from django.http import HttpResponse
from django.template import loader

def html_file_view(request):
    template = loader.get_template('runsheets/my_html_file.html')
    html_content = template.render()
    return HttpResponse(html_content, content_type='text/html')








class AddRunsheetDataView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            model_name = data.get('model_name')
            model_data = data.get('data')

            runsheet_models = {
                'Runsheet1': Runsheet1,
                'Runsheet2': Runsheet2,
                'Runsheet3': Runsheet3,
                'Runsheet4': Runsheet4,
                'Runsheet5': Runsheet5,
                'Runsheet6': Runsheet6,
                'Runsheet7': Runsheet7,
                'Runsheet8': Runsheet8,
            }

            if not model_name or model_name not in runsheet_models:
                return JsonResponse({'error': 'Invalid model name'}, status=400)

            model_class = runsheet_models[model_name]
            driver_instance = User.objects.get(id=model_data['driver_id'])

            passenger_name = model_data.get('passenger_name')
            if passenger_name:
                passenger_instance, created = Passenger.objects.get_or_create(name=passenger_name, defaults={})
            else:
                passenger_instance = None  # Handle this case as needed

            model_data.pop('passenger_name', None)  # Remove passenger_name key from model_data

            instance = model_class(driver=driver_instance, **model_data)
            if passenger_instance:
                instance.passenger_name = passenger_instance
            instance.save()

            return JsonResponse({'message': 'Data added successfully'}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class PassengerFilterView(APIView):
    def get(self, request, user_id):
        try:
            passengers = Passenger.objects.filter(user_id=user_id)
            serializer = PassengerSerializer(passengers, many=True)
            return Response(serializer.data)
        except Passenger.DoesNotExist:
            return Response({'error': 'Passenger not found'}, status=404)
class ShiftTimeListAPIView(APIView):
    def get(self, request):
        shift_times = ShiftTime.objects.all()
        serializer = ShiftTimeSerializer(shift_times, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def runsheet1_driver_view(request, pk):
    try:
        instances = Runsheet1.objects.filter(driver__id=pk)
        serializer = Runsheet1Serializer(instances, many=True)
        data = serializer.data
        if data:
            response_data = {
                'success': True,
                'message': f'Data retrieved successfully for driver ID: {pk}.',
                'data': data
            }
            return Response(response_data, status=200)
        else:
            response_data = {
                'success': False,
                'message': f'No data found for driver ID: {pk}.'
            }
            return Response(response_data, status=404)
    except Runsheet1.DoesNotExist:
        response_data = {
            'success': False,
            'message': 'Driver not found in the Runsheet1 table.'
        }
        return Response(response_data, status=404)

# class Runsheet1CreateAPIView(APIView):
#     def post(self, request):
#         serializer = Runsheet1Serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['PUT'])
# def bulk_update_runsheet1(request):
#     print("faarta-------> ",request.data)
#     serializer = Runsheet1BulkUpdateSerializer(data=request.data,many=True)
#     if serializer.is_valid(raise_exception=False):
#         serializer.save()



#         return Response({"success": True, "message": "Bulk update successful"})
#     else:
#         print("erroorr ",serializer.errors)
#         return Response({"success": False, "message": "No updates provided."})
# from rest_framework import status

# @api_view(['PUT'])
# def bulk_update_runsheet1(request):
#     print("faarta-------> ", request.data)
#     serializer = Runsheet1BulkUpdateSerializer(data=request.data, many=True)

#     if serializer.is_valid():
#         serializer.save()
#         return Response({"success": True, "message": "Bulk update successful"})
#     else:
#         print("erroorr ", serializer.errors)
#         return Response(
#             {"success": False, "message": "Validation error.", "errors": serializer.errors},
#             status=status.HTTP_400_BAD_REQUEST
#         )
# class Runsheet1BulkUpdateView(ListAPIView):
#     serializer_class = Runsheet1Serializer

#     def put(self, request, *args, **kwargs):
#         # Get the list of data from the request payload
#         data = request.data

#         # Get the list of primary keys to be updated
#         primary_keys = [item['pk'] for item in data]

#         # Fetch the instances to be updated from the database
#         runsheets = Runsheet1.objects.filter(pk__in=primary_keys)

#         # Update each instance with the provided data
#         for item in data:
#             run_id = item['pk']
#             runsheet = runsheets.get(pk=run_id)
#             serializer = self.get_serializer(runsheet, data=item, partial=True)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()

#         return Response({"message": "Bulk update successful."})

########bulkupdate
class Runsheet1BulkUpdateAPIView(ListCreateAPIView):
    serializer_class = Runsheet1Serializer

    def get_queryset(self):
        # Return an empty queryset, as we don't need any pre-existing data
        return Runsheet1.objects.none()

    def create(self, request, *args, **kwargs):
        # Check if the user has already created a record today
        today = timezone.now().date()
        if Runsheet1.objects.filter(created_date=today, user=request.user).exists():
            return Response({'message': 'A record has already been created today.'},
                            status=status.HTTP_403_FORBIDDEN)

        # Get the list of data from the request
        data = request.data

        # Create a list to hold the new and updated instances
        updated_runsheets = []

        # Loop through the data and update or create instances
        for item in data:
            runsheet_id = item.get('id')
            if runsheet_id:
                try:
                    # Try to get the existing runsheet instance
                    runsheet = Runsheet1.objects.get(pk=runsheet_id)

                    # Update the fields
                    runsheet.Morning_price = item.get('Morning_price', runsheet.Morning_price)
                    runsheet.Evening_price = item.get('Evening_price', runsheet.Evening_price)

                    # Save the updated runsheet
                    runsheet.save()

                    updated_runsheets.append(runsheet)
                except Runsheet1.DoesNotExist:
                    # If the runsheet with the given ID does not exist, skip it
                    pass
            else:
                # Create a new runsheet record
                runsheet = Runsheet1.objects.create(
                    Morning_price=item.get('Morning_price'),
                    Evening_price=item.get('Evening_price'),
                    created_date=today,
                    user=request.user
                )
                updated_runsheets.append(runsheet)

        # Serialize the updated and new runsheets
        serializer = self.get_serializer(updated_runsheets, many=True)

        # Customize the response structure
        response_data = serializer.data

        return Response(response_data, status=status.HTTP_200_OK)
# class Runsheet1BulkUpdateAPIView(ListCreateAPIView):
#     serializer_class = Runsheet1Serializer

#     def get_queryset(self):
#         # Return an empty queryset, as we don't need any pre-existing data
#         return Runsheet1.objects.none()

#     def create(self, request, *args, **kwargs):
#         # Get the list of data from the request
#         data = request.data

#         # Create a list to hold the updated instances
#         updated_runsheets = []

#         # Loop through the data and update the corresponding instances
#         for item in data:
#             runsheet_id = item.get('id')
#             try:
#                 # Try to get the existing runsheet instance
#                 runsheet = Runsheet1.objects.get(pk=runsheet_id)

#                 # Update the Morning_price and Evening_price fields
#                 runsheet.Morning_price = item.get('Morning_price', runsheet.Morning_price)
#                 runsheet.Evening_price = item.get('Evening_price', runsheet.Evening_price)

#                 # Save the updated runsheet
#                 runsheet.save()

#                 updated_runsheets.append(runsheet)
#             except Runsheet1.DoesNotExist:
#                 # If the runsheet with the given ID does not exist, skip it
#                 pass

#         # Serialize the updated runsheets
#         serializer = self.get_serializer(updated_runsheets, many=True)

#         # Customize the response structure
#         response_data = serializer.data

#         return Response(response_data, status=status.HTTP_200_OK)

# class Runsheet2BulkUpdateAPIView(ListCreateAPIView):
#     serializer_class = Runsheet2Serializer

#     def get_queryset(self):
#         # Return an empty queryset, as we don't need any pre-existing data
#         return Runsheet1.objects.none()

#     def create(self, request, *args, **kwargs):
#         # Get the list of data from the request
#         data = request.data

#         # Create a list to hold the updated instances
#         updated_runsheets = []

#         # Loop through the data and update the corresponding instances
#         for item in data:
#             runsheet_id = item.get('id')
#             try:
#                 # Try to get the existing runsheet instance
#                 runsheet = Runsheet2.objects.get(pk=runsheet_id)

#                 # Update the Morning_price and Evening_price fields
#                 runsheet.Morning_price = item.get('Morning_price', runsheet.Morning_price)
#                 runsheet.Evening_price = item.get('Evening_price', runsheet.Evening_price)

#                 # Save the updated runsheet
#                 runsheet.save()

#                 updated_runsheets.append(runsheet)
#             except Runsheet2.DoesNotExist:
#                 # If the runsheet with the given ID does not exist, skip it
#                 pass

#         # Serialize the updated runsheets
#         serializer = self.get_serializer(updated_runsheets, many=True)

#         # Customize the response structure
#         response_data = serializer.data

#         return Response(response_data, status=status.HTTP_200_OK)
class Runsheet2BulkUpdateAPIView(ListCreateAPIView):
    serializer_class = Runsheet2Serializer

    def get_queryset(self):
        # Return an empty queryset, as we don't need any pre-existing data
        return Runsheet2.objects.none()

    def create(self, request, *args, **kwargs):
        # Check if the user has already created a record today
        today = timezone.now().date()
        if Runsheet2.objects.filter(created_date=today, user=request.user).exists():
            return Response({'message': 'A record has already been created today.'},
                            status=status.HTTP_403_FORBIDDEN)

        # Get the list of data from the request
        data = request.data

        # Create a list to hold the new and updated instances
        updated_runsheets = []

        # Loop through the data and update or create instances
        for item in data:
            runsheet_id = item.get('id')
            if runsheet_id:
                try:
                    # Try to get the existing runsheet instance
                    runsheet = Runsheet2.objects.get(pk=runsheet_id)

                    # Update the fields
                    runsheet.Morning_price = item.get('Morning_price', runsheet.Morning_price)
                    runsheet.Evening_price = item.get('Evening_price', runsheet.Evening_price)

                    # Save the updated runsheet
                    runsheet.save()

                    updated_runsheets.append(runsheet)
                except Runsheet2.DoesNotExist:
                    # If the runsheet with the given ID does not exist, skip it
                    pass
            else:
                # Create a new runsheet record
                runsheet = Runsheet2.objects.create(
                    Morning_price=item.get('Morning_price'),
                    Evening_price=item.get('Evening_price'),
                    created_date=today,
                    user=request.user
                )
                updated_runsheets.append(runsheet)

        # Serialize the updated and new runsheets
        serializer = self.get_serializer(updated_runsheets, many=True)

        # Customize the response structure
        response_data = serializer.data

        return Response(response_data, status=status.HTTP_200_OK)


# class Runsheet3BulkUpdateAPIView(ListCreateAPIView):
#     serializer_class = Runsheet3Serializer

#     def get_queryset(self):
#         # Return an empty queryset, as we don't need any pre-existing data
#         return Runsheet3.objects.none()

#     def create(self, request, *args, **kwargs):
#         # Get the list of data from the request
#         data = request.data

#         # Create a list to hold the updated instances
#         updated_runsheets = []

#         # Loop through the data and update the corresponding instances
#         for item in data:
#             runsheet_id = item.get('id')
#             try:
#                 # Try to get the existing runsheet instance
#                 runsheet = Runsheet3.objects.get(pk=runsheet_id)

#                 # Update the Morning_price and Evening_price fields
#                 runsheet.Morning_price = item.get('Morning_price', runsheet.Morning_price)
#                 runsheet.Evening_price = item.get('Evening_price', runsheet.Evening_price)

#                 # Save the updated runsheet
#                 runsheet.save()

#                 updated_runsheets.append(runsheet)
#             except Runsheet3.DoesNotExist:
#                 # If the runsheet with the given ID does not exist, skip it
#                 pass

#         # Serialize the updated runsheets
#         serializer = self.get_serializer(updated_runsheets, many=True)

#         # Customize the response structure
#         response_data = serializer.data

#         return Response(response_data, status=status.HTTP_200_OK)
class Runsheet3BulkUpdateAPIView(ListCreateAPIView):
    serializer_class = Runsheet3Serializer

    def get_queryset(self):
        # Return an empty queryset, as we don't need any pre-existing data
        return Runsheet3.objects.none()

    def create(self, request, *args, **kwargs):
        # Check if the user has already created a record today
        today = timezone.now().date()
        if Runsheet3.objects.filter(created_date=today, user=request.user).exists():
            return Response({'message': 'A record has already been created today.'},
                            status=status.HTTP_403_FORBIDDEN)

        # Get the list of data from the request
        data = request.data

        # Create a list to hold the new and updated instances
        updated_runsheets = []

        # Loop through the data and update or create instances
        for item in data:
            runsheet_id = item.get('id')
            if runsheet_id:
                try:
                    # Try to get the existing runsheet instance
                    runsheet = Runsheet3.objects.get(pk=runsheet_id)

                    # Update the fields
                    runsheet.Morning_price = item.get('Morning_price', runsheet.Morning_price)
                    runsheet.Evening_price = item.get('Evening_price', runsheet.Evening_price)

                    # Save the updated runsheet
                    runsheet.save()

                    updated_runsheets.append(runsheet)
                except Runsheet3.DoesNotExist:
                    # If the runsheet with the given ID does not exist, skip it
                    pass
            else:
                # Create a new runsheet record
                runsheet = Runsheet3.objects.create(
                    Morning_price=item.get('Morning_price'),
                    Evening_price=item.get('Evening_price'),
                    created_date=today,
                    user=request.user
                )
                updated_runsheets.append(runsheet)

        # Serialize the updated and new runsheets
        serializer = self.get_serializer(updated_runsheets, many=True)

        # Customize the response structure
        response_data = serializer.data

        return Response(response_data, status=status.HTTP_200_OK)

# class Runsheet4BulkUpdateAPIView(ListCreateAPIView):
#     serializer_class = Runsheet4Serializer

#     def get_queryset(self):
#         # Return an empty queryset, as we don't need any pre-existing data
#         return Runsheet4.objects.none()

#     def create(self, request, *args, **kwargs):
#         # Get the list of data from the request
#         data = request.data

#         # Create a list to hold the updated instances
#         updated_runsheets = []

#         # Loop through the data and update the corresponding instances
#         for item in data:
#             runsheet_id = item.get('id')
#             try:
#                 # Try to get the existing runsheet instance
#                 runsheet = Runsheet4.objects.get(pk=runsheet_id)

#                 # Update the Morning_price and Evening_price fields
#                 runsheet.Morning_price = item.get('Morning_price', runsheet.Morning_price)
#                 runsheet.Evening_price = item.get('Evening_price', runsheet.Evening_price)

#                 # Save the updated runsheet
#                 runsheet.save()

#                 updated_runsheets.append(runsheet)
#             except Runsheet4.DoesNotExist:
#                 # If the runsheet with the given ID does not exist, skip it
#                 pass

#         # Serialize the updated runsheets
#         serializer = self.get_serializer(updated_runsheets, many=True)

#         # Customize the response structure
#         response_data = serializer.data

#         return Response(response_data, status=status.HTTP_200_OK)
class Runsheet4BulkUpdateAPIView(ListCreateAPIView):
    serializer_class = Runsheet4Serializer

    def get_queryset(self):
        # Return an empty queryset, as we don't need any pre-existing data
        return Runsheet4.objects.none()

    def create(self, request, *args, **kwargs):
        # Check if the user has already created a record today
        today = timezone.now().date()
        if Runsheet4.objects.filter(created_date=today, user=request.user).exists():
            return Response({'message': 'A record has already been created today.'},
                            status=status.HTTP_403_FORBIDDEN)

        # Get the list of data from the request
        data = request.data

        # Create a list to hold the new and updated instances
        updated_runsheets = []

        # Loop through the data and update or create instances
        for item in data:
            runsheet_id = item.get('id')
            if runsheet_id:
                try:
                    # Try to get the existing runsheet instance
                    runsheet = Runsheet4.objects.get(pk=runsheet_id)

                    # Update the fields
                    runsheet.Morning_price = item.get('Morning_price', runsheet.Morning_price)
                    runsheet.Evening_price = item.get('Evening_price', runsheet.Evening_price)

                    # Save the updated runsheet
                    runsheet.save()

                    updated_runsheets.append(runsheet)
                except Runsheet4.DoesNotExist:
                    # If the runsheet with the given ID does not exist, skip it
                    pass
            else:
                # Create a new runsheet record
                runsheet = Runsheet4.objects.create(
                    Morning_price=item.get('Morning_price'),
                    Evening_price=item.get('Evening_price'),
                    created_date=today,
                    user=request.user
                )
                updated_runsheets.append(runsheet)

        # Serialize the updated and new runsheets
        serializer = self.get_serializer(updated_runsheets, many=True)

        # Customize the response structure
        response_data = serializer.data

        return Response(response_data, status=status.HTTP_200_OK)
# class Runsheet5BulkUpdateAPIView(ListCreateAPIView):
#     serializer_class = Runsheet5Serializer

#     def get_queryset(self):
#         # Return an empty queryset, as we don't need any pre-existing data
#         return Runsheet5.objects.none()

#     def create(self, request, *args, **kwargs):
#         # Get the list of data from the request
#         data = request.data

#         # Create a list to hold the updated instances
#         updated_runsheets = []

#         # Loop through the data and update the corresponding instances
#         for item in data:
#             runsheet_id = item.get('id')
#             try:
#                 # Try to get the existing runsheet instance
#                 runsheet = Runsheet5.objects.get(pk=runsheet_id)

#                 # Update the Morning_price and Evening_price fields
#                 runsheet.Morning_price = item.get('Morning_price', runsheet.Morning_price)
#                 runsheet.Evening_price = item.get('Evening_price', runsheet.Evening_price)

#                 # Save the updated runsheet
#                 runsheet.save()

#                 updated_runsheets.append(runsheet)
#             except Runsheet5.DoesNotExist:
#                 # If the runsheet with the given ID does not exist, skip it
#                 pass

#         # Serialize the updated runsheets
#         serializer = self.get_serializer(updated_runsheets, many=True)

#         # Customize the response structure
#         response_data = serializer.data

#         return Response(response_data, status=status.HTTP_200_OK)
class Runsheet5BulkUpdateAPIView(ListCreateAPIView):
    serializer_class = Runsheet5Serializer

    def get_queryset(self):
        # Return an empty queryset, as we don't need any pre-existing data
        return Runsheet5.objects.none()

    def create(self, request, *args, **kwargs):
        # Check if the user has already created a record today
        today = timezone.now().date()
        if Runsheet5.objects.filter(created_date=today, user=request.user).exists():
            return Response({'message': 'A record has already been created today.'},
                            status=status.HTTP_403_FORBIDDEN)

        # Get the list of data from the request
        data = request.data

        # Create a list to hold the new and updated instances
        updated_runsheets = []

        # Loop through the data and update or create instances
        for item in data:
            runsheet_id = item.get('id')
            if runsheet_id:
                try:
                    # Try to get the existing runsheet instance
                    runsheet = Runsheet5.objects.get(pk=runsheet_id)

                    # Update the fields
                    runsheet.Morning_price = item.get('Morning_price', runsheet.Morning_price)
                    runsheet.Evening_price = item.get('Evening_price', runsheet.Evening_price)

                    # Save the updated runsheet
                    runsheet.save()

                    updated_runsheets.append(runsheet)
                except Runsheet5.DoesNotExist:
                    # If the runsheet with the given ID does not exist, skip it
                    pass
            else:
                # Create a new runsheet record
                runsheet = Runsheet5.objects.create(
                    Morning_price=item.get('Morning_price'),
                    Evening_price=item.get('Evening_price'),
                    created_date=today,
                    user=request.user
                )
                updated_runsheets.append(runsheet)

        # Serialize the updated and new runsheets
        serializer = self.get_serializer(updated_runsheets, many=True)

        # Customize the response structure
        response_data = serializer.data

        return Response(response_data, status=status.HTTP_200_OK)

# class Runsheet6BulkUpdateAPIView(ListCreateAPIView):
#     serializer_class = Runsheet1Serializer

#     def get_queryset(self):
#         # Return an empty queryset, as we don't need any pre-existing data
#         return Runsheet6.objects.none()

#     def create(self, request, *args, **kwargs):
#         # Get the list of data from the request
#         data = request.data

#         # Create a list to hold the updated instances
#         updated_runsheets = []

#         # Loop through the data and update the corresponding instances
#         for item in data:
#             runsheet_id = item.get('id')
#             try:
#                 # Try to get the existing runsheet instance
#                 runsheet = Runsheet6.objects.get(pk=runsheet_id)

#                 # Update the Morning_price and Evening_price fields
#                 runsheet.Morning_price = item.get('Morning_price', runsheet.Morning_price)
#                 runsheet.Evening_price = item.get('Evening_price', runsheet.Evening_price)

#                 # Save the updated runsheet
#                 runsheet.save()

#                 updated_runsheets.append(runsheet)
#             except Runsheet6.DoesNotExist:
#                 # If the runsheet with the given ID does not exist, skip it
#                 pass

#         # Serialize the updated runsheets
#         serializer = self.get_serializer(updated_runsheets, many=True)

#         # Customize the response structure
#         response_data = serializer.data

#         return Response(response_data, status=status.HTTP_200_OK)

class Runsheet6BulkUpdateAPIView(ListCreateAPIView):
    serializer_class = Runsheet6Serializer  # Changed to Runsheet6Serializer

    def get_queryset(self):
        # Return an empty queryset, as we don't need any pre-existing data
        return Runsheet6.objects.none()  # Changed to Runsheet6

    def create(self, request, *args, **kwargs):
        # Check if the user has already created a record today
        today = timezone.now().date()
        if Runsheet6.objects.filter(created_date=today, user=request.user).exists():
            return Response({'message': 'A record has already been created today.'},
                            status=status.HTTP_403_FORBIDDEN)

        # Get the list of data from the request
        data = request.data

        # Create a list to hold the new and updated instances
        updated_runsheets = []

        # Loop through the data and update or create instances
        for item in data:
            runsheet_id = item.get('id')
            if runsheet_id:
                try:
                    # Try to get the existing runsheet instance
                    runsheet = Runsheet6.objects.get(pk=runsheet_id)  # Changed to Runsheet6

                    # Update the fields
                    runsheet.Morning_price = item.get('Morning_price', runsheet.Morning_price)
                    runsheet.Evening_price = item.get('Evening_price', runsheet.Evening_price)

                    # Save the updated runsheet
                    runsheet.save()

                    updated_runsheets.append(runsheet)
                except Runsheet6.DoesNotExist:  # Changed to Runsheet6
                    # If the runsheet with the given ID does not exist, skip it
                    pass
            else:
                # Create a new runsheet record
                runsheet = Runsheet6.objects.create(  # Changed to Runsheet6
                    Morning_price=item.get('Morning_price'),
                    Evening_price=item.get('Evening_price'),
                    created_date=today,
                    user=request.user
                )
                updated_runsheets.append(runsheet)

        # Serialize the updated and new runsheets
        serializer = self.get_serializer(updated_runsheets, many=True)

        # Customize the response structure
        response_data = serializer.data

        return Response(response_data, status=status.HTTP_200_OK)


# class Runsheet7BulkUpdateAPIView(ListCreateAPIView):
#     serializer_class = Runsheet7Serializer

#     def get_queryset(self):
#         # Return an empty queryset, as we don't need any pre-existing data
#         return Runsheet7.objects.none()

#     def create(self, request, *args, **kwargs):
#         # Get the list of data from the request
#         data = request.data

#         # Create a list to hold the updated instances
#         updated_runsheets = []

#         # Loop through the data and update the corresponding instances
#         for item in data:
#             runsheet_id = item.get('id')
#             try:
#                 # Try to get the existing runsheet instance
#                 runsheet = Runsheet7.objects.get(pk=runsheet_id)

#                 # Update the Morning_price and Evening_price fields
#                 runsheet.Morning_price = item.get('Morning_price', runsheet.Morning_price)
#                 runsheet.Evening_price = item.get('Evening_price', runsheet.Evening_price)

#                 # Save the updated runsheet
#                 runsheet.save()

#                 updated_runsheets.append(runsheet)
#             except Runsheet7.DoesNotExist:
#                 # If the runsheet with the given ID does not exist, skip it
#                 pass

#         # Serialize the updated runsheets
#         serializer = self.get_serializer(updated_runsheets, many=True)

#         # Customize the response structure
#         response_data = serializer.data

#         return Response(response_data, status=status.HTTP_200_OK)
class Runsheet7BulkUpdateAPIView(ListCreateAPIView):
    serializer_class = Runsheet7Serializer

    def get_queryset(self):
        # Return an empty queryset, as we don't need any pre-existing data
        return Runsheet7.objects.none()

    def create(self, request, *args, **kwargs):
        # Check if the user has already created a record today
        today = timezone.now().date()
        if Runsheet7.objects.filter(created_date=today, user=request.user).exists():
            return Response({'message': 'A record has already been created today.'},
                            status=status.HTTP_403_FORBIDDEN)

        # Get the list of data from the request
        data = request.data

        # Create a list to hold the new and updated instances
        updated_runsheets = []

        # Loop through the data and update or create instances
        for item in data:
            runsheet_id = item.get('id')
            if runsheet_id:
                try:
                    # Try to get the existing runsheet instance
                    runsheet = Runsheet7.objects.get(pk=runsheet_id)

                    # Update the fields
                    runsheet.Morning_price = item.get('Morning_price', runsheet.Morning_price)
                    runsheet.Evening_price = item.get('Evening_price', runsheet.Evening_price)

                    # Save the updated runsheet
                    runsheet.save()

                    updated_runsheets.append(runsheet)
                except Runsheet7.DoesNotExist:
                    # If the runsheet with the given ID does not exist, skip it
                    pass
            else:
                # Create a new runsheet record
                runsheet = Runsheet7.objects.create(
                    Morning_price=item.get('Morning_price'),
                    Evening_price=item.get('Evening_price'),
                    created_date=today,
                    user=request.user
                )
                updated_runsheets.append(runsheet)

        # Serialize the updated and new runsheets
        serializer = self.get_serializer(updated_runsheets, many=True)

        # Customize the response structure
        response_data = serializer.data

        return Response(response_data, status=status.HTTP_200_OK)

# class Runsheet8BulkUpdateAPIView(ListCreateAPIView):
#     serializer_class = Runsheet1Serializer

#     def get_queryset(self):
#         # Return an empty queryset, as we don't need any pre-existing data
#         return Runsheet8.objects.none()

#     def create(self, request, *args, **kwargs):
#         # Get the list of data from the request
#         data = request.data

#         # Create a list to hold the updated instances
#         updated_runsheets = []

#         # Loop through the data and update the corresponding instances
#         for item in data:
#             runsheet_id = item.get('id')
#             try:
#                 # Try to get the existing runsheet instance
#                 runsheet = Runsheet8.objects.get(pk=runsheet_id)

#                 # Update the Morning_price and Evening_price fields
#                 runsheet.Morning_price = item.get('Morning_price', runsheet.Morning_price)
#                 runsheet.Evening_price = item.get('Evening_price', runsheet.Evening_price)

#                 # Save the updated runsheet
#                 runsheet.save()

#                 updated_runsheets.append(runsheet)
#             except Runsheet8.DoesNotExist:
#                 # If the runsheet with the given ID does not exist, skip it
#                 pass

#         # Serialize the updated runsheets
#         serializer = self.get_serializer(updated_runsheets, many=True)

#         # Customize the response structure
#         response_data = serializer.data

#         return Response(response_data, status=status.HTTP_200_OK)





class Runsheet8BulkUpdateAPIView(ListCreateAPIView):
    serializer_class = Runsheet1Serializer

    def get_queryset(self):
        # Return an empty queryset, as we don't need any pre-existing data
        return Runsheet8.objects.none()

    def create(self, request, *args, **kwargs):
        # Check if the user has already created a record today
        today = timezone.now().date()
        if Runsheet8.objects.filter(created_date=today, user=request.user).exists():
            return Response({'message': 'A record has already been created today.'},
                            status=status.HTTP_403_FORBIDDEN)

        # Get the list of data from the request
        data = request.data

        # Create a list to hold the new and updated instances
        updated_runsheets = []

        # Loop through the data and update or create instances
        for item in data:
            runsheet_id = item.get('id')
            if runsheet_id:
                try:
                    # Try to get the existing runsheet instance
                    runsheet = Runsheet8.objects.get(pk=runsheet_id)

                    # Update the fields
                    runsheet.Morning_price = item.get('Morning_price', runsheet.Morning_price)
                    runsheet.Evening_price = item.get('Evening_price', runsheet.Evening_price)

                    # Save the updated runsheet
                    runsheet.save()

                    updated_runsheets.append(runsheet)
                except Runsheet8.DoesNotExist:
                    # If the runsheet with the given ID does not exist, skip it
                    pass
            else:
                # Create a new runsheet record
                runsheet = Runsheet8.objects.create(
                    Morning_price=item.get('Morning_price'),
                    Evening_price=item.get('Evening_price'),
                    created_date=today,
                    user=request.user
                )
                updated_runsheets.append(runsheet)

        # Serialize the updated and new runsheets
        serializer = self.get_serializer(updated_runsheets, many=True)

        # Customize the response structure
        response_data = serializer.data

        return Response(response_data, status=status.HTTP_200_OK)





####get list of user
class AssignPassengerByDriverrunsheet1APIView(ListAPIView):
    serializer_class = AssignPassengerToRunsheet1Serializer

    def get_queryset(self):
        # Get the driver_id from the URL parameter
        driver_id = self.kwargs['driver_id']

        # Filter the queryset to retrieve passenger assignments for the given driver_id
        queryset = AssignPassengerToRunsheet1.objects.filter(user_id=driver_id)

        return queryset




class AssignPassengerByDriverrunsheet2APIView(ListAPIView):
    serializer_class = AssignPassengerToRunsheet2Serializer

    def get_queryset(self):
        # Get the driver_id from the URL parameter
        driver_id = self.kwargs['driver_id']

        # Filter the queryset to retrieve passenger assignments for the given driver_id
        queryset = AssignPassengerToRunsheet2.objects.filter(user_id=driver_id)

        return queryset
class AssignPassengerByDriverrunsheet3APIView(ListAPIView):
    serializer_class = AssignPassengerToRunsheet3Serializer

    def get_queryset(self):
        # Get the driver_id from the URL parameter
        driver_id = self.kwargs['driver_id']

        # Filter the queryset to retrieve passenger assignments for the given driver_id
        queryset = AssignPassengerToRunsheet3.objects.filter(user_id=driver_id)

        return queryset
class AssignPassengerByDriverrunsheet4APIView(ListAPIView):
    serializer_class = AssignPassengerToRunsheet4Serializer

    def get_queryset(self):
        # Get the driver_id from the URL parameter
        driver_id = self.kwargs['driver_id']

        # Filter the queryset to retrieve passenger assignments for the given driver_id
        queryset = AssignPassengerToRunsheet4.objects.filter(user_id=driver_id)

        return queryset
class AssignPassengerByDriverrunsheet5APIView(ListAPIView):
    serializer_class = AssignPassengerToRunsheet5Serializer

    def get_queryset(self):
        # Get the driver_id from the URL parameter
        driver_id = self.kwargs['driver_id']

        # Filter the queryset to retrieve passenger assignments for the given driver_id
        queryset = AssignPassengerToRunsheet5.objects.filter(user_id=driver_id)

        return queryset
class AssignPassengerByDriverrunsheet6APIView(ListAPIView):
    serializer_class = AssignPassengerToRunsheet6Serializer

    def get_queryset(self):
        # Get the driver_id from the URL parameter
        driver_id = self.kwargs['driver_id']

        # Filter the queryset to retrieve passenger assignments for the given driver_id
        queryset = AssignPassengerToRunsheet6.objects.filter(user_id=driver_id)

        return queryset
class AssignPassengerByDriverrunsheet7APIView(ListAPIView):
    serializer_class = AssignPassengerToRunsheet7Serializer

    def get_queryset(self):
        # Get the driver_id from the URL parameter
        driver_id = self.kwargs['driver_id']

        # Filter the queryset to retrieve passenger assignments for the given driver_id
        queryset = AssignPassengerToRunsheet7.objects.filter(user_id=driver_id)

        return queryset
class AssignPassengerByDriverrunsheet8APIView(ListAPIView):
    serializer_class = AssignPassengerToRunsheet8Serializer

    def get_queryset(self):
        # Get the driver_id from the URL parameter
        driver_id = self.kwargs['driver_id']

        # Filter the queryset to retrieve passenger assignments for the given driver_id
        queryset = AssignPassengerToRunsheet8.objects.filter(user_id=driver_id)

        return queryset
@api_view(['POST'])
def create_runsheet1_bulk(request):
    data = request.data
    today = timezone.now().date()
    passenger_driver_combinations = set()  # To keep track of passenger-driver combinations for the current date

    # Check if any record exists for the current date with the same passenger-driver combination
    existing_records = Runsheet1.objects.filter(date_created__date=today)
    for record in existing_records:
        combination = (record.passenger_name.id, record.driver.id)
        passenger_driver_combinations.add(combination)

    new_records = []
    for item in data:
        passenger_id = item.get('passenger_name', None)
        driver_id = item.get('driver', None)
        combination = (passenger_id, driver_id)
        if combination in passenger_driver_combinations:
            return Response({'success': False, 'message': f'Record for this passenger   already exists for today. Duplicate records not allowed.'}, status=400)
        else:
            new_records.append(item)

    # If no records exist for the current date with the same passenger-driver combination, proceed with creating new records
    serializer = Runsheet1Serializer(data=new_records, many=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'success': True, 'message': 'Records have been saved successfully.'}, status=201)
    return Response({'success': False, 'message': serializer.errors}, status=400)


@api_view(['POST'])
def create_runsheet2_bulk(request):
    data = request.data
    today = timezone.now().date()
    passenger_driver_combinations = set()  # To keep track of passenger-driver combinations for the current date

    # Check if any record exists for the current date with the same passenger-driver combination
    existing_records = Runsheet2.objects.filter(date_created__date=today)
    for record in existing_records:
        combination = (record.passenger_name.id, record.driver.id)
        passenger_driver_combinations.add(combination)

    new_records = []
    for item in data:
        passenger_id = item.get('passenger_name', None)
        driver_id = item.get('driver', None)
        combination = (passenger_id, driver_id)
        if combination in passenger_driver_combinations:
            return Response({'success': False, 'message': f'Record for this passenger   already exists for today. Duplicate records not allowed.'}, status=400)
        else:
            new_records.append(item)

    # If no records exist for the current date with the same passenger-driver combination, proceed with creating new records
    serializer = Runsheet2Serializer(data=new_records, many=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'success': True, 'message': 'Records have been saved successfully.'}, status=201)
    return Response({'success': False, 'message': serializer.errors}, status=400)



@api_view(['POST'])
def create_runsheet3_bulk(request):
    data = request.data
    today = timezone.now().date()
    passenger_driver_combinations = set()  # To keep track of passenger-driver combinations for the current date

    # Check if any record exists for the current date with the same passenger-driver combination
    existing_records = Runsheet3.objects.filter(date_created__date=today)
    for record in existing_records:
        combination = (record.passenger_name.id, record.driver.id)
        passenger_driver_combinations.add(combination)

    new_records = []
    for item in data:
        passenger_id = item.get('passenger_name', None)
        driver_id = item.get('driver', None)
        combination = (passenger_id, driver_id)
        if combination in passenger_driver_combinations:
            return Response({'success': False, 'message': f'Record for this passenger   already exists for today. Duplicate records not allowed.'}, status=400)
        else:
            new_records.append(item)

    # If no records exist for the current date with the same passenger-driver combination, proceed with creating new records
    serializer = Runsheet3Serializer(data=new_records, many=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'success': True, 'message': 'Records have been saved successfully.'}, status=201)
    return Response({'success': False, 'message': serializer.errors}, status=400)




@api_view(['POST'])
def create_runsheet4_bulk(request):
    data = request.data
    today = timezone.now().date()
    passenger_driver_combinations = set()  # To keep track of passenger-driver combinations for the current date

    # Check if any record exists for the current date with the same passenger-driver combination
    existing_records = Runsheet4.objects.filter(date_created__date=today)
    for record in existing_records:
        combination = (record.passenger_name.id, record.driver.id)
        passenger_driver_combinations.add(combination)

    new_records = []
    for item in data:
        passenger_id = item.get('passenger_name', None)
        driver_id = item.get('driver', None)
        combination = (passenger_id, driver_id)
        if combination in passenger_driver_combinations:
            return Response({'success': False, 'message': f'Record for this passenger   already exists for today. Duplicate records not allowed.'}, status=400)
        else:
            new_records.append(item)

    # If no records exist for the current date with the same passenger-driver combination, proceed with creating new records
    serializer = Runsheet4Serializer(data=new_records, many=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'success': True, 'message': 'Records have been saved successfully.'}, status=201)
    return Response({'success': False, 'message': serializer.errors}, status=400)


@api_view(['POST'])
def create_runsheet5_bulk(request):
    data = request.data
    today = timezone.now().date()
    passenger_driver_combinations = set()  # To keep track of passenger-driver combinations for the current date

    # Check if any record exists for the current date with the same passenger-driver combination
    existing_records = Runsheet5.objects.filter(date_created__date=today)
    for record in existing_records:
        combination = (record.passenger_name.id, record.driver.id)
        passenger_driver_combinations.add(combination)

    new_records = []
    for item in data:
        passenger_id = item.get('passenger_name', None)
        driver_id = item.get('driver', None)
        combination = (passenger_id, driver_id)
        if combination in passenger_driver_combinations:
            return Response({'success': False, 'message': f'Record for this passenger   already exists for today. Duplicate records not allowed.'}, status=400)
        else:
            new_records.append(item)

    # If no records exist for the current date with the same passenger-driver combination, proceed with creating new records
    serializer = Runsheet5Serializer(data=new_records, many=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'success': True, 'message': 'Records have been saved successfully.'}, status=201)
    return Response({'success': False, 'message': serializer.errors}, status=400)




@api_view(['POST'])
def create_runsheet6_bulk(request):
    data = request.data
    today = timezone.now().date()
    passenger_driver_combinations = set()  # To keep track of passenger-driver combinations for the current date

    # Check if any record exists for the current date with the same passenger-driver combination
    existing_records = Runsheet6.objects.filter(date_created__date=today)
    for record in existing_records:
        combination = (record.passenger_name.id, record.driver.id)
        passenger_driver_combinations.add(combination)

    new_records = []
    for item in data:
        passenger_id = item.get('passenger_name', None)
        driver_id = item.get('driver', None)
        combination = (passenger_id, driver_id)
        if combination in passenger_driver_combinations:
            return Response({'success': False, 'message': f'Record for this passenger   already exists for today. Duplicate records not allowed.'}, status=400)
        else:
            new_records.append(item)

    # If no records exist for the current date with the same passenger-driver combination, proceed with creating new records
    serializer = Runsheet6Serializer(data=new_records, many=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'success': True, 'message': 'Records have been saved successfully.'}, status=201)
    return Response({'success': False, 'message': serializer.errors}, status=400)



@api_view(['POST'])
def create_runsheet7_bulk(request):
    data = request.data
    today = timezone.now().date()
    passenger_driver_combinations = set()  # To keep track of passenger-driver combinations for the current date

    # Check if any record exists for the current date with the same passenger-driver combination
    existing_records = Runsheet7.objects.filter(date_created__date=today)
    for record in existing_records:
        combination = (record.passenger_name.id, record.driver.id)
        passenger_driver_combinations.add(combination)

    new_records = []
    for item in data:
        passenger_id = item.get('passenger_name', None)
        driver_id = item.get('driver', None)
        combination = (passenger_id, driver_id)
        if combination in passenger_driver_combinations:
            return Response({'success': False, 'message': f'Record for this passenger   already exists for today. Duplicate records not allowed.'}, status=400)
        else:
            new_records.append(item)

    # If no records exist for the current date with the same passenger-driver combination, proceed with creating new records
    serializer = Runsheet7Serializer(data=new_records, many=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'success': True, 'message': 'Records have been saved successfully.'}, status=201)
    return Response({'success': False, 'message': serializer.errors}, status=400)





@api_view(['POST'])
def create_runsheet8_bulk(request):
    data = request.data
    today = timezone.now().date()
    passenger_driver_combinations = set()  # To keep track of passenger-driver combinations for the current date

    # Check if any record exists for the current date with the same passenger-driver combination
    existing_records = Runsheet8.objects.filter(date_created__date=today)
    for record in existing_records:
        combination = (record.passenger_name.id, record.driver.id)
        passenger_driver_combinations.add(combination)

    new_records = []
    for item in data:
        passenger_id = item.get('passenger_name', None)
        driver_id = item.get('driver', None)
        combination = (passenger_id, driver_id)
        if combination in passenger_driver_combinations:
            return Response({'success': False, 'message': f'Record for this passenger   already exists for today. Duplicate records not allowed.'}, status=400)
        else:
            new_records.append(item)

    # If no records exist for the current date with the same passenger-driver combination, proceed with creating new records
    serializer = Runsheet8Serializer(data=new_records, many=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'success': True, 'message': 'Records have been saved successfully.'}, status=201)
    return Response({'success': False, 'message': serializer.errors}, status=400)









@api_view(['POST'])
def create_help_and_dispute(request):
    serializer = HelpAndDisputeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'success': True, 'message': 'Help and Dispute record has been created successfully.'}, status=201)
    return Response({'success': False, 'message': serializer.errors}, status=400)
#######get recors





@api_view(['GET'])
def get_driver_records1(request, driver_id):
    runsheets = Runsheet1.objects.filter(driver__id=driver_id)

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

        runsheet_data = {
            'id': runsheet.id,  # Include the runsheet ID
            'passenger_name': passenger_name,
            'formatted_date_created': formatted_date,
            'Morning_price': runsheet.Morning_price,
            'Evening_price': runsheet.Evening_price,
            'driver': driver_name,
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

    if not runsheet_array:
        response_data['message'] = 'No records found for the given driver.'

    return Response(response_data, status=status.HTTP_200_OK)




@api_view(['GET'])
def get_driver_records2(request, driver_id):
    runsheets = Runsheet2.objects.filter(driver__id=driver_id)

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

        runsheet_data = {
            'id': runsheet.id,  # Include the runsheet ID
            'passenger_name': passenger_name,
            'formatted_date_created': formatted_date,
            'Morning_price': runsheet.Morning_price,
            'Evening_price': runsheet.Evening_price,
            'driver': driver_name,
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

    if not runsheet_array:
        response_data['message'] = 'No records found for the given driver.'

    return Response(response_data, status=status.HTTP_200_OK)


# @api_view(['GET'])
# def get_driver_records2(request, driver_id):
#     runsheets = Runsheet2.objects.filter(driver__id=driver_id)

#     if not runsheets.exists():
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     runsheets = runsheets.annotate(date=TruncDate('date_created')).order_by('date')
#     runsheet_array = []
#     total_morning_all = 0
#     total_evening_all = 0
#     grouped_runsheets = {}

#     for runsheet in runsheets:
#         date = runsheet.date
#         formatted_date = date.strftime("%A %d/%m/%Y")
#         passenger_name = runsheet.passenger_name.name  # Assuming name is a field in the Passenger model
#         driver_name = runsheet.driver.name  # Assuming name is a field in the User model

#         runsheet_data = {
#             'id': runsheet.id,  # Include the runsheet ID
#             'passenger_name': passenger_name,
#             'formatted_date_created': formatted_date,
#             'Morning_price': runsheet.Morning_price,
#             'Evening_price': runsheet.Evening_price,
#             'driver': driver_name,
#         }

#         if formatted_date in grouped_runsheets:
#             grouped_runsheets[formatted_date]['runsheets'].append(runsheet_data)
#             grouped_runsheets[formatted_date]['total_morning_price'] += runsheet.Morning_price if runsheet.Morning_price is not None else 0
#             grouped_runsheets[formatted_date]['total_evening_price'] += runsheet.Evening_price if runsheet.Evening_price is not None else 0
#         else:
#             grouped_runsheets[formatted_date] = {
#                 'formatted_date_created': formatted_date,
#                 'runsheets': [runsheet_data],
#                 'total_morning_price': runsheet.Morning_price if runsheet.Morning_price is not None else 0,
#                 'total_evening_price': runsheet.Evening_price if runsheet.Evening_price is not None else 0,
#             }

#         total_morning_all += runsheet.Morning_price if runsheet.Morning_price is not None else 0
#         total_evening_all += runsheet.Evening_price if runsheet.Evening_price is not None else 0

#     for date_key in grouped_runsheets:
#         runsheet_array.append(grouped_runsheets[date_key])

#     # Add overall totals to the response data
#     response_data = {
#         'grouped_runsheets': runsheet_array,
#         'total_morning_all': total_morning_all,
#         'total_evening_all': total_evening_all,
#     }

#     return Response(response_data)




@api_view(['GET'])
def get_driver_records3(request, driver_id):
    runsheets = Runsheet3.objects.filter(driver__id=driver_id)

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

        runsheet_data = {
            'id': runsheet.id,  # Include the runsheet ID
            'passenger_name': passenger_name,
            'formatted_date_created': formatted_date,
            'Morning_price': runsheet.Morning_price,
            'Evening_price': runsheet.Evening_price,
            'driver': driver_name,
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

    if not runsheet_array:
        response_data['message'] = 'No records found for the given driver.'

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_driver_records4(request, driver_id):
    runsheets = Runsheet4.objects.filter(driver__id=driver_id)

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

        runsheet_data = {
            'id': runsheet.id,  # Include the runsheet ID
            'passenger_name': passenger_name,
            'formatted_date_created': formatted_date,
            'Morning_price': runsheet.Morning_price,
            'Evening_price': runsheet.Evening_price,
            'driver': driver_name,
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

    if not runsheet_array:
        response_data['message'] = 'No records found for the given driver.'

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_driver_records5(request, driver_id):
    runsheets = Runsheet5.objects.filter(driver__id=driver_id)

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

        runsheet_data = {
            'id': runsheet.id,  # Include the runsheet ID
            'passenger_name': passenger_name,
            'formatted_date_created': formatted_date,
            'Morning_price': runsheet.Morning_price,
            'Evening_price': runsheet.Evening_price,
            'driver': driver_name,
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

    if not runsheet_array:
        response_data['message'] = 'No records found for the given driver.'

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_driver_records6(request, driver_id):
    runsheets = Runsheet6.objects.filter(driver__id=driver_id)

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

        runsheet_data = {
            'id': runsheet.id,  # Include the runsheet ID
            'passenger_name': passenger_name,
            'formatted_date_created': formatted_date,
            'Morning_price': runsheet.Morning_price,
            'Evening_price': runsheet.Evening_price,
            'driver': driver_name,
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

    if not runsheet_array:
        response_data['message'] = 'No records found for the given driver.'

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_driver_records7(request, driver_id):
    runsheets = Runsheet7.objects.filter(driver__id=driver_id)

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

        runsheet_data = {
            'id': runsheet.id,  # Include the runsheet ID
            'passenger_name': passenger_name,
            'formatted_date_created': formatted_date,
            'Morning_price': runsheet.Morning_price,
            'Evening_price': runsheet.Evening_price,
            'driver': driver_name,
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

    if not runsheet_array:
        response_data['message'] = 'No records found for the given driver.'

    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_driver_records8(request, driver_id):
    runsheets = Runsheet8.objects.filter(driver__id=driver_id)

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

        runsheet_data = {
            'id': runsheet.id,  # Include the runsheet ID
            'passenger_name': passenger_name,
            'formatted_date_created': formatted_date,
            'Morning_price': runsheet.Morning_price,
            'Evening_price': runsheet.Evening_price,
            'driver': driver_name,
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

    if not runsheet_array:
        response_data['message'] = 'No records found for the given driver.'

    return Response(response_data, status=status.HTTP_200_OK)



# class RunsheetSumView(APIView):
#     def get(self, request, driver_id):
#         try:
#             today = timezone.now().date()
#             start_of_week = today - timedelta(days=today.weekday())
#             end_of_week = start_of_week + timedelta(days=6)

#             runsheet_model = Runsheet1

#             # Check if any records exist for the driver (without date filter)
#             test_records = runsheet_model.objects.filter(driver_id=driver_id)
#             if not test_records.exists():
#                 return Response({'error': 'No records found for this driver in any week.'})

#             # Proceed with the filtered query
#             morning_sum = (
#                 runsheet_model.objects.filter(driver_id=driver_id, date_created__range=[start_of_week, end_of_week])
#                 .aggregate(total=Sum('Morning_price'))['total'] or Decimal('0.00')
#             )

#             evening_sum = (
#                 runsheet_model.objects.filter(driver_id=driver_id, date_created__range=[start_of_week, end_of_week])
#                 .aggregate(total=Sum('Evening_price'))['total'] or Decimal('0.00')
#             )

#             # Include passenger count and passengers for serializer
#             passenger_count = 0
#             passengers = []

#             # Construct response
#             total_sum = morning_sum + evening_sum

#             data = {
#                 'morning_sum': morning_sum,
#                 'evening_sum': evening_sum,
#                 'total_sum': total_sum,
#                 'passenger_count': passenger_count,
#                 'passengers': passengers,
#             }
#             serializer = RunsheetSumSerializer(data)
#             return Response(serializer.data)

#         except Exception as e:
#             return Response({'error': str(e)})

# class RunsheetSumView(APIView):
#     def get(self, request, driver_id):
#         morning_sum = Decimal('0.00')
#         evening_sum = Decimal('0.00')
#         passenger_data = []

#         runsheet_models = [Runsheet1, Runsheet2, Runsheet3,Runsheet4,Runsheet5,Runsheet6,Runsheet7,Runsheet8 ]  # Add all your Runsheet models here

#         for runsheet_model in runsheet_models:
#             morning_sum += (
#                 runsheet_model.objects.filter(driver_id=driver_id)
#                 .aggregate(total=Sum('Morning_price'))['total'] or Decimal('0.00')
#             )

#             evening_sum += (
#                 runsheet_model.objects.filter(driver_id=driver_id)
#                 .aggregate(total=Sum('Evening_price'))['total'] or Decimal('0.00')
#             )

#             runsheets = runsheet_model.objects.filter(driver_id=driver_id).select_related('passenger_name')
#             for runsheet in runsheets:
#                 passenger_data.append({
#                     'name': runsheet.passenger_name.name,
#                     'address': runsheet.passenger_name.adress,
#                 })

#         total_sum = morning_sum + evening_sum
#         passenger_count = len(passenger_data)

#         data = {
#             'morning_sum': morning_sum,
#             'evening_sum': evening_sum,
#             'total_sum': total_sum,
#             'passenger_count': passenger_count,
#             'passengers': passenger_data,
#         }
#         serializer = RunsheetSumSerializer(data)
#         return Response(serializer.data)
# class RunsheetSumView(APIView):
#     def get(self, request, driver_id):
#         today = timezone.now().date()
#         start_of_week = today - timedelta(days=today.weekday())  # Monday
#         end_of_week = start_of_week + timedelta(days=6)  # Sunday

#         morning_sum = Decimal('0.00')
#         evening_sum = Decimal('0.00')
#         passenger_data = []

#         runsheet_models = [Runsheet1, Runsheet2, Runsheet3, Runsheet4, Runsheet5, Runsheet6, Runsheet7, Runsheet8]

#         for runsheet_model in runsheet_models:
#             morning_sum += (
#                 runsheet_model.objects.filter(driver_id=driver_id, date_created__range=[start_of_week, end_of_week])
#                 .aggregate(total=Sum('Morning_price'))['total'] or Decimal('0.00')
#             )

#             evening_sum += (
#                 runsheet_model.objects.filter(driver_id=driver_id, date_created__range=[start_of_week, end_of_week])
#                 .aggregate(total=Sum('Evening_price'))['total'] or Decimal('0.00')
#             )

#             runsheets = runsheet_model.objects.filter(driver_id=driver_id, date_created__range=[start_of_week, end_of_week]).select_related('passenger_name')
#             for runsheet in runsheets:
#                 passenger_data.append({
#                     'name': runsheet.passenger_name.name,
#                     'address': runsheet.passenger_name.adress,  # Ensure 'adress' is the correct field name
#                 })

#         total_sum = morning_sum + evening_sum
#         passenger_count = len(passenger_data)

#         data = {
#             'morning_sum': morning_sum,
#             'evening_sum': evening_sum,
#             'total_sum': total_sum,
#             'passenger_count': passenger_count,
#             'passengers': passenger_data,
#         }
#         serializer = RunsheetSumSerializer(data)
#         return Response(serializer.data)




class RunsheetSumView(APIView):
    def get(self, request, driver_id):
        try:
            today = timezone.now().date()
            start_of_week = today - timedelta(days=today.weekday())
            end_of_week = start_of_week + timedelta(days=6)

            runsheet_model = Runsheet1

            # Check if any records exist for the driver (without date filter)
            test_records = runsheet_model.objects.filter(driver_id=driver_id)
            if not test_records.exists():
                return Response({'error': 'No records found for this driver in any week.'})

            # Proceed with the filtered query
            morning_sum = (
                runsheet_model.objects.filter(driver_id=driver_id, date_created__date__range=[start_of_week, end_of_week])
                .aggregate(total=Sum('Morning_price'))['total'] or Decimal('0.00')
            )

            evening_sum = (
                runsheet_model.objects.filter(driver_id=driver_id, date_created__date__range=[start_of_week, end_of_week])
                .aggregate(total=Sum('Evening_price'))['total'] or Decimal('0.00')
            )
            passenger_count = runsheet_model.objects.filter(driver_id=driver_id, date_created__date__range=[start_of_week, end_of_week]).count()

            # Construct response

            # Construct response
            total_sum = morning_sum + evening_sum

            # Include passenger count and passengers for serializer

            passengers = []

            # Construct response
            total_sum = morning_sum + evening_sum

            data = {
                'morning_sum': morning_sum,
                'evening_sum': evening_sum,
                'total_sum': total_sum,
                'passenger_count': passenger_count,
                'passengers': passengers,
            }
            serializer = RunsheetSumSerializer(data)
            return Response(serializer.data)

        except Exception as e:
            return Response({'error': str(e)})