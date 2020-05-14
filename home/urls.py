from django.contrib import admin
from django.urls import path
from api.views import api_root
from django.conf.urls import include, url

from django.conf.urls.static import static  #media+static
from django.conf import settings            #media+static
from .views import *
urlpatterns = [
    path('admin/main/main/', main_main),
    path('admin/about/about/', about_about),
    path('admin/about/aboutblock/', about_aboutblock),
    path('admin/districts/districtmain/', districts_districtmain),
    path('admin/districts/district/', districts_district),
    path('admin/mediafiles/mediafiles/', mediafiles_mediafiles),
    path('admin/mediafiles/mediaphotos/', mediafiles_mediaphotos),
    path('admin/main/footerpartners/', main_footerpartners),
    path('admin/opportunities/opportunitiesblock/', opportunities_opportunitiesblock),
    path('admin/news/newsblock/', news_newsblock),
    path('admin/', admin.site.urls),
    url(r'^api/', include('api.urls')),
    url(r'^', include('main.urls')),
]
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
