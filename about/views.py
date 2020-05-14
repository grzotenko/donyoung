from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import *
from .serializers import *
from rest_framework import views
from rest_framework.response import Response
# Create your views here.
class AboutView(views.APIView):
    def get(self, request):
        serializerAbout = AboutSerializer(About.objects.first())
        return Response(serializerAbout.data)