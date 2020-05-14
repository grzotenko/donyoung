from django.shortcuts import render, get_object_or_404
from .models import *
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token
from rest_framework import views, viewsets
from rest_framework import status
from rest_framework.response import Response
from .serializers import SubsSerializer
# Create your views here.

class SubscriptionsEndPoint(views.APIView):
    @csrf_exempt
    def post(self, request, format=None):
        serializer = SubsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

