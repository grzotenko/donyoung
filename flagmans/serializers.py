from rest_framework import serializers
from .models import *

class FlagmansSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flagmans
        fields = ['id', 'title', 'date', 'address','map', 'url']
