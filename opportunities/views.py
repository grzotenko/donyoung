from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import *
from trends.models import Trends
from .serializers import *
from rest_framework import views
from rest_framework.response import Response
from datetime import date, datetime
# Create your views here.
class OpportunitiesAllViewSet(views.APIView):
    def get(self, request, page):
        direction = int(request.GET.get("direction","-1"))
        dateStartStr = request.GET.get("from","-")
        dateEndStr = request.GET.get("to", "-")
        offset = int(page)
        if direction == -1:
            if dateEndStr == "-" and dateStartStr == "-":
                serializerOpportunities = OpportunitiesSerializer(Opportunities.objects.all().reverse()[offset:offset+12], many=True)
            else:
                dateEnd = datetime.strptime(dateEndStr, '%d.%m.%Y')
                dateStart = datetime.strptime(dateStartStr, '%d.%m.%Y')
                setOpportunities = Opportunities.objects.filter(Q(dateEnd__range=(dateStart, dateEnd)) | Q(dateStart__range=(dateStart, dateEnd))).reverse()
                serializerOpportunities = OpportunitiesSerializer(setOpportunities[offset:offset+12], many=True)
        else:
            serializerOpportunities = OpportunitiesSerializer(Opportunities.objects.filter(trends__id = direction).reverse()[offset:offset+12], many=True)

        return Response(dataOpportunities(serializerOpportunities))

class OpportunitiesActiveViewSet(views.APIView):
    def get(self, request, page):
        direction = int(request.GET.get("direction","-1"))
        dateStartStr = request.GET.get("from","-")
        dateEndStr = request.GET.get("to", "-")
        offset = int(page)
        if direction == -1:
            if dateEndStr == "-" and dateStartStr == "-":
                serializerOpportunities = OpportunitiesSerializer(Opportunities.objects.filter(dateEnd__gte = date.today())[offset:offset+12], many=True)
            else:
                dateEnd = datetime.strptime(dateEndStr, '%d.%m.%Y')
                dateStart = datetime.strptime(dateStartStr, '%d.%m.%Y')
                setOpportunities = Opportunities.objects.filter(dateEnd__gte = date.today())
                setOpportunities = setOpportunities.filter(Q(dateEnd__range=(dateStart, dateEnd)) | Q(dateStart__range=(dateStart, dateEnd)))
                serializerOpportunities = OpportunitiesSerializer(setOpportunities[offset:offset+12], many=True)
        else:
            serializerOpportunities = OpportunitiesSerializer(Opportunities.objects.filter(dateEnd__gte = date.today(),trends__id = direction)[offset:offset+12], many=True)
        return Response(dataOpportunities(serializerOpportunities))
class OpportunitiesCompletedViewSet(views.APIView):
    def get(self, request, page):
        direction = int(request.GET.get("direction","-1"))
        dateStartStr = request.GET.get("from","-")
        dateEndStr = request.GET.get("to", "-")
        offset = int(page)
        if direction == -1:
            if dateEndStr == "-" and dateStartStr == "-":
                serializerOpportunities = OpportunitiesSerializer(Opportunities.objects.filter(dateEnd__lt = date.today()).reverse()[offset:offset+12], many=True)
            else:
                dateEnd = datetime.strptime(dateEndStr, '%d.%m.%Y')
                dateStart = datetime.strptime(dateStartStr, '%d.%m.%Y')
                setOpportunities = Opportunities.objects.filter(dateEnd__lt = date.today()).reverse()
                setOpportunities = setOpportunities.filter(Q(dateEnd__range=(dateStart, dateEnd)) | Q(dateStart__range=(dateStart, dateEnd)))
                serializerOpportunities = OpportunitiesSerializer(setOpportunities[offset:offset+12], many=True)
        else:
            serializerOpportunities = OpportunitiesSerializer(Opportunities.objects.filter(dateEnd__lt = date.today(), trends__id = direction).reverse()[offset:offset+12], many=True)
        return Response(dataOpportunities(serializerOpportunities))

def dataOpportunities(serializerOpportunities):
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
        if obj.checkTitle== False:
            opp['title']= None
        opp['image'] = image
    return dataOpp
class OpportunitiesDetail(views.APIView):
    def get(self, request, pk):
        id = int(pk)
        opportunity = get_object_or_404(Opportunities, id=id)
        try:
            next_opportunity = opportunity.get_next_by_dateEnd()
        except:
            next_opportunity = id+1
        try:
            previous_opportunity = opportunity.get_previous_by_dateEnd()
        except:
            previous_opportunity = id-1
        similar_opportunity = list()
        counterSimilarOpportunity = 0
        for trend in opportunity.trends.all():
            for obj in trend.opportunities_set.all():
                if obj.id != opportunity.id:
                    similar_opportunity.append(obj)
                    counterSimilarOpportunity += 1
                if counterSimilarOpportunity == 3:
                    break
            if counterSimilarOpportunity == 3:
                break
        serializerOpportunity = OpportunitySerializer(opportunity)
        serializerOpportunityBlocks = OpportunityBlockSerializer(OpportunitiesBlock.objects.filter(id_fk = opportunity, include = True), many=True)
        serializerNextOpportunity = OpportunityNextPrevSimilarSerializer(next_opportunity)
        serializerPreviousOpportunity = OpportunityNextPrevSimilarSerializer(previous_opportunity)
        serializerSimilarOpportunity = OpportunityNextPrevSimilarSerializer(similar_opportunity, many=True)

        opportunityData = serializerOpportunity.data
        opportunityData['blocks'] = serializerOpportunityBlocks.data
        from image_cropping.utils import get_backend
        image = get_backend().get_thumbnail_url(
            opportunity.imageOld,
            {
                'size': (900, 315),
                'box': opportunity.imageBig,
                'crop': True,
                'detail': True,
            }
        )
        opportunityData['image'] = image

        previousData = None if len(serializerPreviousOpportunity.data) == 0 else serializerPreviousOpportunity.data
        nextData = None if len(serializerNextOpportunity.data) == 0 else serializerNextOpportunity.data

        return Response({
            "opportunity": opportunityData,
            "nextOpportunity": nextData,
            "previousOpportunity": previousData,
            "similarOpportunity": serializerSimilarOpportunity.data,
       })

