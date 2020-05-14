from rest_framework import serializers
from .models import *
from trends.serializers import *


class NewsPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'image', 'date']

class NewsFullSerializer(serializers.Serializer):
    main = NewsPartSerializer(many=True)
    important = NewsPartSerializer(many=True)
class FakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'titlePreview']
class AllNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'titlePreview', 'date']


class AllNewsFullSerializer(serializers.Serializer):
    all_news = AllNewsSerializer(many=True)

class NewsNextPrevSimilarSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title']

class NewsFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsFile
        fields = ['file', 'ext', 'label']


class NewsBlockSerializer(serializers.ModelSerializer):
    newsfile = NewsFileSerializer()
    class Meta:
        model = NewsBlock
        fields = ['id','topLine', 'bottomLine', 'title', 'text', 'newsfile']
class NewsSerializer(serializers.ModelSerializer):
    trends = TrendsSerializer(many=True)
    class Meta:
        model = News
        fields = ['id', 'title', 'date', 'trends', ]