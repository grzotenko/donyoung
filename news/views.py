from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import *
from trends.models import Trends
from .serializers import *
from rest_framework import views
from rest_framework.response import Response
from datetime import date, datetime
# Create your views here.
class NewsDetail(views.APIView):
    def get(self, request, pk):
        id = int(pk)
        news = get_object_or_404(News, id=id)
        try:
            next_news = news.get_next_by_date()
        except:
            next_news = id+1
        try:
            previous_news = news.get_previous_by_date()
        except:
            previous_news = id-1
        similar_news = list()
        counterSimilarNews = 0
        for trend in news.trends.all():
            for obj in trend.news_set.all():
                if obj.id != news.id:
                    similar_news.append(obj)
                    counterSimilarNews+=1
                if counterSimilarNews == 3:
                    break
            if counterSimilarNews == 3:
                break
        from image_cropping.utils import get_backend
        image = get_backend().get_thumbnail_url(
            news.imageOld,
            {
                'size': (900, 315),
                'box': news.imageBig,
                'crop': True,
                'detail': True,
            }
        )
        serializerNews = NewsSerializer(news)
        serializerNewsBlocks = NewsBlockSerializer(NewsBlock.objects.filter(id_fk = news, include = True), many=True)
        serializerNextNews = NewsNextPrevSimilarSerializer(next_news)
        serializerPreviousNews = NewsNextPrevSimilarSerializer(previous_news)
        serializerSimilarNews = NewsNextPrevSimilarSerializer(similar_news, many=True)
        newsData = serializerNews.data
        newsData['blocks'] = serializerNewsBlocks.data
        newsData['image'] = image
        previousData = None if len(serializerPreviousNews.data) == 0 else serializerPreviousNews.data
        nextData = None if len(serializerNextNews.data) == 0 else serializerNextNews.data

        return Response({
            "news": newsData,
            "nextNews": nextData,
            "previousNews": previousData,
            "similarNews": serializerSimilarNews.data,
       })
class AllNewsViewSet(views.APIView):
    def get(self, request, page):
        direction = int(request.GET.get("direction","-1"))
        dateStartStr = request.GET.get("from", "-")
        dateEndStr = request.GET.get("to", "-")
        offset = int(page)
        if direction == -1:
            if dateEndStr == "-" and dateStartStr == "-":
                serializerAllNews = AllNewsSerializer(News.objects.all()[offset:offset + 12],many=True)
            else:
                dateEnd = datetime.strptime(dateEndStr, '%d.%m.%Y')
                dateStart = datetime.strptime(dateStartStr, '%d.%m.%Y')
                setNews = News.objects.filter(date__date__range=(dateStart,dateEnd))
                serializerAllNews = AllNewsSerializer(setNews[offset:offset + 12], many=True)
        else:
            serializerAllNews = AllNewsSerializer(News.objects.filter(trends__id=direction)[offset:offset + 12], many=True)
        newsData = serializerAllNews.data
        from image_cropping.utils import get_backend
        for news in newsData:
            ID = news.get("id")
            obj = News.objects.get(id=ID)
            image = get_backend().get_thumbnail_url(
                obj.imageOld,
                {
                    'size': (900, 315),
                    'box': obj.imageBig,
                    'crop': True,
                    'detail': True,
                }
            )
            news['image'] = image
        return Response(newsData)