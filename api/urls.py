from django.conf.urls import url, include
from django.urls import path
from main.views import MainCommonViewSet, BlockDistrictsViewSetAPI, BlockFlagmansViewSetAPI, BlockMediaViewSetAPI, BlockNewsViewSetAPI, BlockOpportunitiesViewSetAPI, BlockTrendsViewSetAPI
from districts.views import DistrictDetail
from .views import api_root
from flagmans.views import FlagmansActiveViewSet, FlagmansCompletedViewSet
from opportunities.views import OpportunitiesDetail, OpportunitiesAllViewSet, OpportunitiesActiveViewSet, OpportunitiesCompletedViewSet
from trends.views import TrendsDetailNews, TrendsDetailOpportunities, TrendsDetail
from news.views import NewsDetail, AllNewsViewSet
from about.views import AboutView
from searchdon.views import SearchView
from subscriptions.views import SubscriptionsEndPoint
urlpatterns = [
    url(r'^swagger$', api_root),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('common/', MainCommonViewSet.as_view(), name='common-list'),
    path('main/trends/', BlockTrendsViewSetAPI.as_view(), name='main-trends-list'),
    path('main/districts/', BlockDistrictsViewSetAPI.as_view(), name='main-districts-list'),
    path('main/flagmans/', BlockFlagmansViewSetAPI.as_view(), name='main-flagmans-list'),
    path('main/news/', BlockNewsViewSetAPI.as_view(), name='main-news-list'),
    path('main/media/', BlockMediaViewSetAPI.as_view(), name='main-media-list'),
    path('main/opportunities/', BlockOpportunitiesViewSetAPI.as_view(), name='main-opportunities-list'),
    path('districts/<int:pk>', DistrictDetail.as_view(), name='district-detail'),
    path('about/', AboutView.as_view(), name='about-us'),
    path('flagships/active/<int:page>', FlagmansActiveViewSet.as_view(), name='flagmans-active-list'),
    path('flagships/completed/<int:page>', FlagmansCompletedViewSet.as_view(), name='flagmans-completed-list'),
    path('opportunities/active/list/<int:page>', OpportunitiesActiveViewSet.as_view(), name='opportunities-active-list'),
    path('opportunities/completed/list/<int:page>', OpportunitiesCompletedViewSet.as_view(), name='opportunities-completed-list'),
    path('opportunities/all/list/<int:page>', OpportunitiesAllViewSet.as_view(), name='opportunities-all-list'),
    path('opportunities/detail/<int:pk>', OpportunitiesDetail.as_view(), name='opportunities-detail'),
    path('directions/<int:pk>', TrendsDetail.as_view(), name='trends-detail'),
    path('directions/<int:pk>/news/<int:page>', TrendsDetailNews.as_view(), name='trends-detail-news'),
    path('directions/<int:pk>/opportunities/<int:page>', TrendsDetailOpportunities.as_view(), name='trends-detail-opportunities'),
    path('news/detail/<int:pk>', NewsDetail.as_view(), name='news-detail'),
    path('news/list/<int:page>', AllNewsViewSet.as_view(), name='news-list'),
    path('subs/', SubscriptionsEndPoint.as_view(), name='subs-list'),
    path('search/<int:page>', SearchView.as_view(), name='search'),
]
