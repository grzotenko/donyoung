from django.shortcuts import render, get_object_or_404
from .models import Trends,TrendsPartners,TrendsContacts, TrendsDocuments, TrendsHrefs
from .serializers import TrendSerializer, TrendsHrefsSerializer
from news.models import News
from news.serializers import NewsPartSerializer
from opportunities.serializers import OpportunitiesSerializer
from opportunities.models import Opportunities
from rest_framework import views
from rest_framework.response import Response

class TrendsDetail(views.APIView):
    def get(self, request, pk):
        id = int(pk)
        trend = get_object_or_404(Trends, id=id)
        serializerTrend = TrendSerializer(trend).data
        serializerTrend["hrefs"] = TrendsHrefsSerializer(TrendsHrefs.objects.filter(id_fk=trend), many=True).data
        return Response(serializerTrend)


class TrendsDetailNews(views.APIView):
    def get(self, request, pk, page):
        id = int(pk)
        offset = int(page)
        trend = get_object_or_404(Trends, id=id)
        news = News.objects.filter(trends = trend)[offset:offset+6]
        serializerTrendNews = NewsPartSerializer(news, many=True)
        dataTrendNews = serializerTrendNews.data
        from image_cropping.utils import get_backend
        for news in dataTrendNews:
            ID = news.get("id")
            obj = News.objects.get(id=ID)
            image = get_backend().get_thumbnail_url(
                obj.imageOld,
                {
                    'size': (300, 300),
                    'box': obj.image,
                    'crop': True,
                    'detail': True,
                }
            )
            news['image'] = image
        return Response(dataTrendNews)


class TrendsDetailOpportunities(views.APIView):
    def get(self, request, pk, page):
        id = int(pk)
        offset = int(page)
        trend = get_object_or_404(Trends, id=id)
        opportunities = Opportunities.objects.filter(trends = trend)[offset:offset+6]
        serializerTrendOpportunities = OpportunitiesSerializer(opportunities, many=True)
        dataTrendOpp = serializerTrendOpportunities.data
        from image_cropping.utils import get_backend
        for opp in dataTrendOpp:
            ID = opp.get("id")
            obj = Opportunities.objects.get(id=ID)
            image = get_backend().get_thumbnail_url(
                obj.imageOld,
                {
                    'size': (390, 280),
                    'box': obj.image,
                    'crop': True,
                    'detail': True,
                }
            )
            opp['image'] = image
        return Response(serializerTrendOpportunities.data)