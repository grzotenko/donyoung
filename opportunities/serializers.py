from rest_framework import serializers
from .models import *
from trends.serializers import *
class OpportunitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Opportunities
        fields = ['id', 'title', 'date','time', 'address', 'map']

class OpportunityNextPrevSimilarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Opportunities
        fields = ['id', 'title']




class OpportunitiesFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpportunitiesFile
        fields = ['file', 'ext', 'label']
class OpportunityBlockSerializer(serializers.ModelSerializer):
    opportunitiesfile = OpportunitiesFileSerializer()
    class Meta:
        model = OpportunitiesBlock
        fields = ['topLine', 'bottomLine', 'title','text','opportunitiesfile']

class OpportunitySerializer(serializers.ModelSerializer):
    trends = TrendsSerializer(many=True)
    class Meta:
        model = Opportunities
        fields = ['id', 'title', 'date','time', 'address', 'map','trends' ]
