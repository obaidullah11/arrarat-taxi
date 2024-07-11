from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Image
from .serializer import ImageSerializer
from django.shortcuts import get_object_or_404

class GetImageByPublicId(APIView):
    def get(self, request, public_id):
        try:
            image = Image.objects.get(public_id=public_id)
            serializer = ImageSerializer(image)
            return Response(serializer.data)
        except Image.DoesNotExist:
            return Response({'message': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)
class ImageListCreateView(APIView):
    def post(self, request):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ImageRetrieveView(APIView):
    def get(self, request, pk):
        image = get_object_or_404(Image, pk=pk)
        serializer = ImageSerializer(image)
        return Response(serializer.data)

class ImageRetrieveByPublicIdView(APIView):
    def get(self, request, public_id):
        try:
            image = Image.objects.get(public_id=public_id)
        except Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ImageSerializer(image)
        return Response(serializer.data)
