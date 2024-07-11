from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/images/<str:public_id>/', GetImageByPublicId.as_view(), name='get_image_by_public_id'),
    path('api/images/', ImageListCreateView.as_view(), name='image-list-create'),
    path('api/images/<int:pk>/', ImageRetrieveView.as_view(), name='image-retrieve'),
    path('api/images/public_id/<str:public_id>/', ImageRetrieveByPublicIdView.as_view(), name='image-retrieve-by-public-id'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

