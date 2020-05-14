from rest_framework import serializers
from .models import *

class DistrictsMainDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['id', 'title',]

class DistrictsDetailContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DistrictContacts
        fields = ['id', 'name', 'position', 'image', 'email', 'phone']

class DetailAgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields = ['id', 'title', 'text', 'image']

class DistrictsDetailSerializer(serializers.ModelSerializer):
    agency = DetailAgencySerializer()
    # districtcontacts_set = DistrictsDetailContactsSerializer(many=True)
    class Meta:
        model = District
        fields = ['id', 'title', "url", "phone", "address", "map","email", "vk", "instagram", "facebook", 'countYouth', 'percentageYouth', 'agency']


