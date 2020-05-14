from rest_framework import serializers
from .models import *
class TrendsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trends
        fields = ['id', 'title', 'imageActive','imageInactive',]

class TrendsContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrendsContacts
        fields = ['id', 'name','position','phone', 'email','image']

class TrendsHrefsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrendsHrefs
        fields = ['title', 'url']

class TrendsPartnersSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrendsPartners
        fields = ['id', 'title','image', 'url']

class TrendsDocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrendsDocuments
        fields = ['id', 'title','file']

class TrendSerializer(serializers.ModelSerializer):
    trendscontacts_set = TrendsContactsSerializer(many=True)
    trendspartners_set = TrendsPartnersSerializer(many=True)
    trendsdocuments_set = TrendsDocumentsSerializer(many=True)
    class Meta:
        model = Trends
        fields = ['id', 'title', 'text','imageActive','imageInactive', 'trendscontacts_set', 'trendspartners_set', 'trendsdocuments_set']
