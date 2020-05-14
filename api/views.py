from news.serializers import *
from flagmans.serializers import *
from opportunities.serializers import *
from trends.serializers import *
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from datetime import date, timedelta
from collections import namedtuple

objectMain = namedtuple('common', ('main', 'menu', 'organizers', 'social', 'partners', 'contacts', 'massMedia'))
objectNews = namedtuple('main_news', ('main', 'important'))
objectMedia = namedtuple('media', ('photos', 'videos', 'urlphotos', 'urlvideos'))
@api_view(['GET'])
def api_root(request, format=None):
    # opportunitiesCount = Opportunities.objects.all().count() // 12
    # dataOpportunities = {}
    # while opportunitiesCount>=0:
    #     dataOpportunities.update({opportunitiesCount:reverse('opportunities-list', request=request, args=[12*opportunitiesCount])})
    #     opportunitiesCount-=1

    # newsCount = News.objects.all().count() // 12
    # dataNews = {}
    # while newsCount >= 0:
    #     dataNews.update(
    #         {newsCount: reverse('news-list', request=request, args=[12 * newsCount])})
    #     newsCount -= 1

    # flagmansCount = Flagmans.objects.filter(dateEnd__gte = date.today()).count() // 12
    # dataFlagmansActive = {}
    # while flagmansCount >= 0:
    #     dataFlagmansActive.update({flagmansCount: reverse('flagmans-active-list', request=request, args=[12 * flagmansCount])})
    #     flagmansCount -= 1
    #
    # flagmansCount = Flagmans.objects.filter(dateEnd__lt = date.today()).count() // 12
    # dataFlagmansCompleted = {}
    # while flagmansCount >= 0:
    #     dataFlagmansCompleted.update({flagmansCount: reverse('flagmans-completed-list', request=request, args=[12 * flagmansCount])})
    #     flagmansCount -= 1

    # trendsNewsCount = News.objects.filter(trends = Trends.objects.filter(id=1).first()).count() // 12
    # dataDirectionsNews = {}
    # while trendsNewsCount >= 0:
    #     dataDirectionsNews.update({trendsNewsCount: reverse('trends-detail-news', request=request, args=[1, 12 * trendsNewsCount])})
    #     trendsNewsCount -= 1
    #
    # trendsOpportunitiesCount = Opportunities.objects.filter(trends = Trends.objects.filter(id=1).first()).count() // 12
    # dataDirectionsOpportunities = {}
    # while trendsOpportunitiesCount >= 0:
    #     dataDirectionsOpportunities.update({trendsOpportunitiesCount: reverse('trends-detail-opportunities', request=request, args=[1, 12 * trendsOpportunitiesCount])})
    #     trendsOpportunitiesCount -= 1

    return Response({
        'Main Page': {
            'Footer & Header': reverse('common-list', request=request),
            'Block News': reverse('main-news-list', request=request),
            'Block Directions': reverse('main-trends-list', request=request),
            'Block Opportunities': reverse('main-opportunities-list', request=request),
            'Block Districts': reverse('main-districts-list', request=request),
            'Block Flagmans': reverse('main-flagmans-list', request=request),
            'Block Media': reverse('main-media-list', request=request),
        },
        'Opportunities': {
            'Active': {
                'List': reverse('opportunities-active-list', request=request, args=[0]),
                'Filter-Direction': reverse('opportunities-active-list', request=request, args=[0]) + "?direction=1",
                'Filter-Time': reverse('opportunities-active-list', request=request,
                                       args=[0]) + "?from=10.9.2019&to=3.10.2019",
            },
            'Completed': {
                'List': reverse('opportunities-completed-list', request=request, args=[0]),
                'Filter-Direction': reverse('opportunities-completed-list', request=request, args=[0]) + "?direction=1",
                'Filter-Time': reverse('opportunities-completed-list', request=request,
                                       args=[0]) + "?from=10.9.2019&to=3.10.2019",
            },
            'All': {
                'List': reverse('opportunities-all-list', request=request, args=[0]),
                'Filter-Direction': reverse('opportunities-all-list', request=request, args=[0]) + "?direction=1",
                'Filter-Time': reverse('opportunities-all-list', request=request,
                                       args=[0]) + "?from=10.9.2019&to=3.10.2019",
            },
            # 'List-All': reverse('opportunities-all-list', request=request, args=[0]),
            # 'List-Completed': reverse('opportunities-completed-list', request=request, args=[0]),
            # 'List': dataOpportunities.values(),
            # 'Filter-Direction': reverse('opportunities-list-all', request=request, args=[0]) + "?direction=1",
            'Detail': reverse('opportunities-detail', request=request, args=[1]),
            # 'Filter-Time': reverse('opportunities-list', request=request,args=[0]) + "?from=10.09.2019&to=03.10.2019",
        },
        'About us':reverse('about-us', request=request),
        'Test Search': reverse('search', request=request, args=[0]),
        'Subscriptions': reverse('subs-list', request=request),
        'Flagships': {
            'Active': reverse('flagmans-active-list', request=request, args=[0]),
            'Completed': reverse('flagmans-completed-list', request=request, args=[0]),
        },
        'Directions': {
            'Detail': reverse('trends-detail', request=request, args=[1]),
            'News': reverse('trends-detail-news', request=request, args=[1,0]),
            'Opportunities': reverse('trends-detail-opportunities', request=request, args=[1,0]),
        },
        'District': reverse('district-detail', request=request, args=[1]),
        'News': {
            'List': reverse('news-list', request=request, args=[0]),
            'Filter-Direction': reverse('news-list', request=request, args=[0]) + "?direction=1",
            'Detail': reverse('news-detail', request=request, args=[1]),
            'Filter-Time': reverse('news-list', request=request, args=[0]) + "?from=10.09.2019&to=03.10.2019",
        },
    })
