from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [


path('passengers/filter/<int:user_id>/', PassengerFilterView.as_view(), name='passenger_filter'),
path('shift_times/', ShiftTimeListAPIView.as_view(), name='shift_time_list'),
# path('api/runsheet1/driver/<int:driver_id>/', AssignPassengerByDriverAPIView.as_view, name='runsheet1-driver-api'),
path('api/driver/<int:driver_id>/assignments/runsheet1', AssignPassengerByDriverrunsheet1APIView.as_view(), name='assign-passenger-by-driver1'),
path('api/driver/<int:driver_id>/assignments/runsheet2', AssignPassengerByDriverrunsheet2APIView.as_view(), name='assign-passenger-by-driver2'),
path('api/driver/<int:driver_id>/assignments/runsheet3', AssignPassengerByDriverrunsheet3APIView.as_view(), name='assign-passenger-by-driver3'),
path('api/driver/<int:driver_id>/assignments/runsheet4', AssignPassengerByDriverrunsheet4APIView.as_view(), name='assign-passenger-by-driver4'),
path('api/driver/<int:driver_id>/assignments/runsheet5', AssignPassengerByDriverrunsheet5APIView.as_view(), name='assign-passenger-by-driver5'),
path('api/driver/<int:driver_id>/assignments/runsheet6', AssignPassengerByDriverrunsheet6APIView.as_view(), name='assign-passenger-by-driver6'),
path('api/driver/<int:driver_id>/assignments/runsheet7', AssignPassengerByDriverrunsheet7APIView.as_view(), name='assign-passenger-by-driver7'),
path('api/driver/<int:driver_id>/assignments/runsheet8', AssignPassengerByDriverrunsheet8APIView.as_view(), name='assign-passenger-by-driver8'),
path('bulk-update/1', Runsheet1BulkUpdateAPIView.as_view(), name='runsheet-bulk-update1'),
path('bulk-update/2', Runsheet2BulkUpdateAPIView.as_view(), name='runsheet-bulk-update2'),
path('bulk-update/3', Runsheet3BulkUpdateAPIView.as_view(), name='runsheet-bulk-update3'),
path('bulk-update/4', Runsheet4BulkUpdateAPIView.as_view(), name='runsheet-bulk-update4'),
path('bulk-update/5', Runsheet5BulkUpdateAPIView.as_view(), name='runsheet-bulk-update5'),
path('bulk-update/6', Runsheet6BulkUpdateAPIView.as_view(), name='runsheet-bulk-update6'),
path('bulk-update/7', Runsheet7BulkUpdateAPIView.as_view(), name='runsheet-bulk-update7'),
path('bulk-update/8', Runsheet8BulkUpdateAPIView.as_view(), name='runsheet-bulk-update8'),
path('html-file/', html_file_view, name='html-file'),


















path('api/runsheet1/bulk_create', create_runsheet1_bulk, name='runsheet1-bulk-create'),
path('api/runsheet2/bulk_create', create_runsheet2_bulk, name='runsheet1-bulk-create'),
path('api/runsheet3/bulk_create', create_runsheet3_bulk, name='runsheet1-bulk-create'),
path('api/runsheet4/bulk_create', create_runsheet4_bulk, name='runsheet1-bulk-create'),
path('api/runsheet5/bulk_create', create_runsheet5_bulk, name='runsheet1-bulk-create'),
path('api/runsheet6/bulk_create', create_runsheet6_bulk, name='runsheet1-bulk-create'),
path('api/runsheet7/bulk_create', create_runsheet7_bulk, name='runsheet1-bulk-create'),
path('api/runsheet8/bulk_create', create_runsheet8_bulk, name='runsheet1-bulk-create'),














path('helpanddispute/create/', create_help_and_dispute, name='create_help_and_dispute'),


path('api/runsheet1/<int:driver_id>/', get_driver_records1, name='runsheet-driver-detail'),
path('api/runsheet2/<int:driver_id>/', get_driver_records2, name='runsheet-driver-detail'),
path('api/runsheet3/<int:driver_id>/', get_driver_records3, name='runsheet-driver-detail'),
path('api/runsheet4/<int:driver_id>/', get_driver_records4, name='runsheet-driver-detail'),
path('api/runsheet5/<int:driver_id>/', get_driver_records5, name='runsheet-driver-detail'),
path('api/runsheet6/<int:driver_id>/', get_driver_records6, name='runsheet-driver-detail'),
path('api/runsheet7/<int:driver_id>/', get_driver_records7, name='runsheet-driver-detail'),
path('api/runsheet8/<int:driver_id>/', get_driver_records8, name='runsheet-driver-detail'),

path('api/runsheet-summary/<int:driver_id>/', RunsheetSumView.as_view(), name='runsheet-summary'),




path('api/add_runsheet_data/', AddRunsheetDataView.as_view(), name='add_runsheet_data'),



]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)






# http://127.0.0.1:8000/helpanddispute/create/    for create help and dispute

# response for get request     #http://127.0.0.1:8000/api/driver/1/assignments/runsheet1    1 is driver id for get list
# [
#     {
#         "id": 1,
#         "user": 1,
#         "passenger": 2,
#         "date_created": "2023-07-29T15:10:12.216729Z",
#         "passenger_name": "pasenger2"
#     },
#     {
#         "id": 3,
#         "user": 1,
#         "passenger": 1,
#         "date_created": "2023-07-29T17:37:13.376278Z",
#         "passenger_name": "passenger"
#     },
#     {
#         "id": 4,
#         "user": 1,
#         "passenger": 3,
#         "date_created": "2023-07-29T17:37:24.040005Z",
#         "passenger_name": "passenger for driver2"
#     }
# ]
##########################################
#http://127.0.0.1:8000/api/runsheet1/bulk_create  is use for bulk create body for it

# [
#   {
#     "passenger_name": 3,
#     "Morning_price": 10.0,
#     "Evening_price": 15.0,
#     "driver": 1
#   },
# {
#     "passenger_name": 1,
#     "Morning_price": 10.0,
#     "Evening_price": 15.0,
#     "driver": 1
#   },
#   {
#     "passenger_name": 2,
#     "Morning_price": 8.0,
#     "Evening_price": 12.0,
#     "driver": 1
#   }
# ]


# http://127.0.0.1:8000/helpanddispute/create/    for create help and dispute

########################################################
# {
#     "complaint": "This is a sample complaint.",
#     "driver": 1
# }



