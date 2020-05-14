from rest_framework import serializers
from .models import *

class SubsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subs
        fields = ['id', 'email']

