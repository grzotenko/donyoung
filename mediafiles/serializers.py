from rest_framework import serializers
from .models import *



class MediaPhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaPhotos
        fields = ['id', 'title', 'url']

class MediaVideosSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaVideos
        fields = ['id', 'title', 'url']

class MediaFullSerializer(serializers.Serializer):
    photos = MediaPhotosSerializer(many=True)
    videos = MediaVideosSerializer(many=True)
    urlphotos = serializers.CharField(max_length=201)
    urlvideos = serializers.CharField(max_length=201)