from django.shortcuts import render
from django.views import View
from .serializers import *
from news.serializers import *
from districts.serializers import *
from districts.models import *
from flagmans.serializers import *
from mediafiles.serializers import *
from opportunities.serializers import *
from trends.serializers import *
from trends.models import Trends
from rest_framework import views
from rest_framework.response import Response
from datetime import date, timedelta
from api.views import objectMedia,objectMain,objectNews

class MainCommonViewSet(views.APIView):
    def get(self, request):
        ObjectMain = objectMain(
            main=Main.objects.first(),
            menu=HeaderMenu.objects.all(),
            organizers=HeaderOrganizers.objects.all(),
            social=SocialNet.objects.first(),
            partners=FooterPartners.objects.all(),
            contacts=FooterContacts.objects.first(),
            massMedia=FooterContacts.objects.last(),
        )
        serializerCommon = CommonSerializer(ObjectMain)
        serializerCommon.data.get("menu")[4].update({"path": "/direction/" + str(Trends.objects.first().id) +"/about"})
        commonData = serializerCommon.data
        from image_cropping.utils import get_backend
        for partner in commonData.get("partners"):
            ID = partner.get("id")
            obj = FooterPartners.objects.get(id=ID)
            image = get_backend().get_thumbnail_url(
                obj.imageOld,
                {
                    'size': (50, 50),
                    'box': obj.image,
                    'crop': True,
                    'detail': True,
                }
            )
            partner['image'] = image

        return Response(serializerCommon.data)
class BlockFlagmansViewSetAPI(views.APIView):
    def get(self, request):
        serializerFlagmans = FlagmansSerializer(Flagmans.objects.filter(dateEnd__gte=date.today()), many=True)
        dataFlagmans = serializerFlagmans.data
        from image_cropping.utils import get_backend
        for flagman in dataFlagmans:
            ID = flagman.get("id")
            obj = Flagmans.objects.get(id=ID)
            image = get_backend().get_thumbnail_url(
                obj.imageOld,
                {
                    'size': (320, 300),
                    'box': obj.image,
                    'crop': True,
                    'detail': True,
                }
            )
            flagman['image'] = image
        return Response(dataFlagmans)
class BlockNewsViewSetAPI(views.APIView):
    def get(self, request):
        ObjectNews = objectNews(
            main=News.objects.filter(main=True)[:5],
            important=News.objects.filter(important=True)[:5],
        )
        serializerNews = NewsFullSerializer(ObjectNews)
        newsData = serializerNews.data
        from image_cropping.utils import get_backend
        for news in newsData.get("main"):
            ID = news.get("id")
            obj = News.objects.get(id = ID)
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
        for news in newsData.get("important"):
            ID = news.get("id")
            obj = News.objects.get(id = ID)
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
        return Response(newsData)
class BlockMediaViewSetAPI(views.APIView):
    def get(self, request):
        ObjectMedia = objectMedia(
            photos=MediaPhotos.objects.all(),
            videos=MediaVideos.objects.all(),
            urlphotos=MediaFiles.objects.first().urlPhotos,
            urlvideos=MediaFiles.objects.first().urlVideos,
        )


        serializerMedia = MediaFullSerializer(ObjectMedia)
        mediaData = serializerMedia.data
        from image_cropping.utils import get_backend
        for media in mediaData.get("photos"):
            ID = media.get("id")
            obj = MediaPhotos.objects.get(id = ID)
            image = get_backend().get_thumbnail_url(
                obj.imageOld,
                {
                    'size': (280, 140),
                    'box': obj.image,
                    'crop': True,
                    'detail': True,
                }
            )
            media['image'] = image
        return Response(mediaData)
class BlockOpportunitiesViewSetAPI(views.APIView):
    def get(self, request):
        serializerOpportunities = OpportunitiesSerializer(Opportunities.objects.filter(main = True), many=True)
        dataOpp = serializerOpportunities.data
        from image_cropping.utils import get_backend
        for opp in dataOpp:
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
            if obj.checkTitle == False:
                opp['title'] = None
            opp['image'] = image
        return Response(dataOpp)

class BlockTrendsViewSetAPI(views.APIView):
    def get(self, request):
        serializerTrends = TrendsSerializer(Trends.objects.all(), many=True)
        return Response(serializerTrends.data)
class BlockDistrictsViewSetAPI(views.APIView):
    def get(self, request):
        districtData = dict()
        districtData['cities'] = DistrictsMainDetailSerializer(District.objects.filter(isCity = True), many=True).data
        districtData['districts'] = DistrictsMainDetailSerializer(District.objects.filter(isCity = False), many=True).data
        return Response(districtData)

class mainView(View):
    template_name = 'index.html'
    def get(self, request):#, *args, **kwargs):
        context = dict()
        return render(request, self.template_name, context)
