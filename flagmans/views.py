from django.shortcuts import render, get_object_or_404
from .models import *
from .serializers import *
from rest_framework import views
from rest_framework.response import Response
from datetime import date
# Create your views here.
class FlagmansActiveViewSet(views.APIView):
    def get(self, request, page):
        offset = int(page)
        serializerFlagmans = FlagmansSerializer(Flagmans.objects.filter(dateEnd__gte = date.today())[offset:offset+12], many=True)
        return Response(dataFlagmans(serializerFlagmans))

class FlagmansCompletedViewSet(views.APIView):
    def get(self, request, page):
        offset = int(page)
        serializerFlagmans = FlagmansSerializer(Flagmans.objects.filter(dateEnd__lt = date.today()).reverse()[offset:offset+12], many=True)
        return Response(dataFlagmans(serializerFlagmans))
def dataFlagmans(serializerFlagmans):
    dataFlagman = serializerFlagmans.data
    from image_cropping.utils import get_backend
    for flagman in dataFlagman:
        ID = flagman.get("id")
        obj = Flagmans.objects.get(id=ID)
        image = get_backend().get_thumbnail_url(
            obj.imageOld,
            {
                'size': (320, 300),
                'box': obj.image,
                'crop': True,
                'detail': True,
            }
        )
        flagman['image'] = image
    return dataFlagman
