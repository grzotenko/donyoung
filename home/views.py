from django.shortcuts import render
from django.shortcuts import redirect
from main.models import Main
from mediafiles.models import MediaFiles
from about.models import About
from districts.models import DistrictMain
# Create your views here.
def main_main(request):
    return redirect("/admin/main/main/"+str(Main.objects.first().id)+"/change/")
def about_about(request):
    return redirect("/admin/about/about/"+str(About.objects.first().id)+"/change/")
def districts_districtmain(request):
    return redirect("/admin/districts/districtmain/"+str(DistrictMain.objects.first().id)+"/change/")
def districts_district(request):
    return redirect("/admin/districts/districtmain/"+str(DistrictMain.objects.first().id)+"/change/#tabs-2")
def about_aboutblock(request):
    return redirect("/admin/about/about/"+str(About.objects.first().id)+"/change/#tabs-2")
def mediafiles_mediafiles(request):
    return redirect("/admin/mediafiles/mediafiles/"+str(MediaFiles.objects.first().id)+"/change/")
def mediafiles_mediaphotos(request):
    return redirect("/admin/mediafiles/mediafiles/"+str(MediaFiles.objects.first().id)+"/change/#tabs-2")
def main_footerpartners(request):
    return redirect("/admin/main/main/"+str(Main.objects.first().id)+"/change/#tabs-6")
def opportunities_opportunitiesblock(request):
    return redirect("/admin/opportunities/opportunities/")
def news_newsblock(request):
    return redirect("/admin/news/news/")
