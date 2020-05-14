from rest_framework import serializers
from .models import *
class AboutPeopleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutBlockPeople
        fields = ['id', 'name','position','email','phone','image']
class AboutBlockSerializer(serializers.ModelSerializer):
    aboutblockpeople_set= AboutPeopleSerializer(many = True)
    class Meta:
        model = AboutBlock
        fields = ['id', 'title','aboutblockpeople_set']
class AboutSerializer(serializers.ModelSerializer):
    aboutblock_set = AboutBlockSerializer(many = True)
    class Meta:
        model = About
        fields = ['work_time', 'text','email','phone', 'map','address','aboutblock_set']