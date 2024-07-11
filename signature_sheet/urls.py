from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
path('api/driver/<int:driver_id>/assignments/signature_sheet1', AssignPassengerByDriversignaturesheetAPIView.as_view(), name='assign-passenger-by-driver1'),
path('api/add_signature_sheet1/',add_signature_sheet, name='add_signature_sheet'),
path('get_driver_records1/signaturesheet1/<int:driver_id>/', get_driver_records1, name='get_driver_records1'),
path('api/createsignaturereceipt/', create_signature_receipt),
path('api/upload-signature/<int:pk>/', create_signature_image_receipt),
path('api/allsignature-receipts/', SignatureReceiptListCreateView.as_view(), name='signature_receipt_list_create'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





# http://127.0.0.1:8000/digitalrunssheet/api/driver/13/assignments/signature_sheet1
# [] 
#  {
#     "id": 1,
#     "user": 13,
#     "passenger": 11,
#     "date_created": "2023-09-18T02:57:11.367165+10:00",
#     "passenger_name": "John Doe"
#   },
#   {
#     "id": 2,
#     "user": 13,
#     "passenger": 12,
#     "date_created": "2023-09-18T02:57:21.948866+10:00",
#     "passenger_name": " Doe"
#   }
# ]
