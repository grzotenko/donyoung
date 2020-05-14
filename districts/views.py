from django.shortcuts import render, get_object_or_404
from .models import *
from .serializers import *
from rest_framework import views
from rest_framework.response import Response
# Create your views here.
class DistrictDetail(views.APIView):
    def get(self, request, pk):
        PK = int(pk)
        district = get_object_or_404(District, id=PK)
        serializerDistrict = DistrictsDetailSerializer(district)
        dataDistrict = serializerDistrict.data
        listFull = list()
        deps = Department.objects.filter(id_fk = district)
        for dep in deps:
            dictDep = dict()
            dictDep["title"] = dep.title
            dictDep["contacts"] = DistrictsDetailContactsSerializer(DistrictContacts.objects.filter(department = dep), many=True).data
            listFull.append(dictDep)
        dataDistrict["districtcontacts_set"] = listFull
        return Response(dataDistrict)