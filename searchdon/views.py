from django.shortcuts import render, get_object_or_404
from news.models import News, NewsBlock
from flagmans.models import Flagmans
from opportunities.models import Opportunities, OpportunitiesBlock
from districts.models import District, DistrictContacts, Agency, Department
from .models import SettingsSearch
from trends.models import Trends, TrendsContacts
from django.db.models import Q, Sum
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, TrigramSimilarity
from rest_framework import views
from rest_framework.response import Response
from datetime import date, datetime
import re
def SortByRank(listEntry):
    return listEntry['rank']

def ResultDictBuilder(result_dict):
    r_array = list()
    keys = result_dict.keys()
    for key in keys:
        r_array.append(result_dict.get(key))
    r_array.sort(reverse=True, key=SortByRank)
    for r in r_array:
        del r["rank"]
    return r_array
class SearchView(views.APIView):
    def get(self, request, page):
        offset = int(page)
        result_dict = dict()
        dominantEssence = request.GET.get("p", "-")
        settings = SettingsSearch.objects.first()
        # =====================================================================================================
        # ======================================== Parse input string =========================================
        # =====================================================================================================
        query = request.GET.get("q","-")
        query = query.translate(str.maketrans("", "", "!@#$%^&*_+|+\/:;[]{}<>,."))
        query = re.sub( '\s+', ' ', query).strip()
        if query == "направления":
            i = 100
            for entry in Trends.objects.all():
                result_dict['/opportunity/' + str(entry.id)] = {
                    'id': entry.id,
                    'rank': i,
                    'title': entry.title,
                    'titlePreview': None,
                    'type': 'opportunity'
                }
                i -= 1
        elif query == "территории":
            i = 100
            for entry in District.objects.all():
                result_dict['/territory/' + str(entry.id)] = {
                    'id': entry.id,
                    'rank': i,
                    'title': entry.title,
                    'titlePreview': None,
                    'type': 'territory'
                }
                i -= 1
        elif query == "флагманы":
            i = 0
            for entry in Flagmans.objects.all():
                result_dict['/flagship/' + str(entry.id)] = {
                    'id': entry.id,
                    'rank': i,
                    'title': entry.title,
                    'titlePreview': None,
                    'type': 'flagship'
                }
                i -= 1
        elif query == "новости":
            i = 0
            for entry in News.objects.all():
                result_dict['/news/' + str(entry.id)] = {
                    'id': entry.id,
                    'rank': i,
                    'title': entry.title,
                    'titlePreview': None,
                    'type': 'news'
                }
                i -= 1
        elif query == "возможности":
            i = 0
            for entry in Opportunities.objects.all():
                result_dict['/opportunity/' + str(entry.id)] = {
                    'id': entry.id,
                    'rank': i,
                    'title': entry.title,
                    'titlePreview': None,
                    'type': 'opportunity'
                }
                i -= 1
        else:
            query_dict = query.split(" ")
            len_dict = len(query_dict)
            i = 1
            while i < len_dict:
                j = 0
                while j < len_dict-i:
                    word = ""
                    l = 0
                    while l <= i:
                        word += query_dict[l+j] + " "
                        l+=1
                    query_dict.append(word[:-1])
                    j+=1
                i+=1
            # =====================================================================================================
            # =================================== Search query inside News ========================================
            # =====================================================================================================
            vectorTitle = SearchVector('title')
            vectorPreview = SearchVector('titlePreview')
            vector = SearchVector('title') + SearchVector('text')
            for word in query_dict:
                que = SearchQuery(word)
                news_temp = News.objects.annotate(qTitle=SearchRank(vectorTitle, que), qPreview=SearchRank(vectorPreview, que))
                for entry in news_temp:
                    entry.rank = round(entry.qTitle * settings.factorTitle + entry.qPreview * settings.factorPreview, 4)
                    news_blocks_sum = NewsBlock.objects.filter(id_fk=entry, include=True).annotate(similarity=SearchRank(vector, que)).exclude(similarity__lte = 0).aggregate(Sum('similarity'))
                    if news_blocks_sum['similarity__sum'] is None:
                        news_blocks_sum['similarity__sum'] = 0
                    entry.rank += round(news_blocks_sum['similarity__sum'] * settings.factorText, 4)
                    if entry.rank >= settings.filterGTE:
                        if dominantEssence == "news":
                            entry.rank += settings.factorPage
                        result_dict['/news/' + str(entry.id)] = {
                            'id': entry.id,
                            'rank': entry.rank,
                            'title': entry.title,
                            'titlePreview': entry.titlePreview,
                            'type': 'news'
                        }
            # =====================================================================================================
            # =============================== Search query inside Opportunities ===================================
            # =====================================================================================================
            vectorTitle = SearchVector('title')
            vector = SearchVector('title') + SearchVector('text')
            for word in query_dict:
                que = SearchQuery(word)
                opp_temp = Opportunities.objects.annotate(qTitle=SearchRank(vectorTitle, que))
                for entry in opp_temp:
                    entry.rank = round(entry.qTitle * (settings.factorTitle + settings.factorPreview), 4)
                    opp_blocks_sum = OpportunitiesBlock.objects.filter(id_fk=entry, include=True).annotate(
                        similarity=SearchRank(
                            vector, que)).exclude(similarity__lte=0).aggregate(Sum('similarity'))
                    if opp_blocks_sum['similarity__sum'] is None:
                        opp_blocks_sum['similarity__sum'] = 0
                    entry.rank += round(opp_blocks_sum['similarity__sum'] * settings.factorText, 4)
                    if entry.rank >= settings.filterGTE:
                        if dominantEssence == "opportunity":
                            entry.rank += settings.factorPage
                        result_dict['/opportunity/' + str(entry.id)] = {
                            'id': entry.id,
                            'rank': entry.rank,
                            'title': entry.title,
                            'titlePreview': None,
                            'type': 'opportunity'
                        }
            # =====================================================================================================
            # =================================== Search query inside Flagmans ====================================
            # =====================================================================================================
            vectorTitle = SearchVector('title')
            vectorAddress = SearchVector('address')
            vectorDate = SearchVector('date')
            for word in query_dict:
                que = SearchQuery(word)
                flagship_temp = Flagmans.objects.annotate(qTitle=SearchRank(vectorTitle, que), qText=SearchRank(vectorAddress, que)+SearchRank(vectorDate, que))
                for entry in flagship_temp:
                    entry.rank = round(entry.qTitle * settings.factorTitle + entry.qText * settings.factorPreview, 4)
                    if entry.rank >= settings.filterGTE:
                        if dominantEssence == "flagship":
                            entry.rank += settings.factorPage
                        result_dict['/flagship/' + str(entry.id)] = {
                            'id': entry.id,
                            'rank': entry.rank,
                            'title': entry.title,
                            'titlePreview': None,
                            'type': 'flagship'
                        }

            # =====================================================================================================
            # =================================== Search query inside Districts ===================================
            # =====================================================================================================
            vectorContacts = SearchVector('name') + SearchVector('position')
            vectorAgency = SearchVector('title') + SearchVector('text')
            vectorDepartment = SearchVector('title')
            vectorTitle = SearchVector('title')
            for word in query_dict:
                que = SearchQuery(word)
                district_temp = District.objects.annotate(qTitle=SearchRank(vectorTitle, que))
                for entry in district_temp:
                    entry.rank = round(entry.qTitle * settings.factorText, 4)
                    dContacts_sum = DistrictContacts.objects.filter(id_fk=entry).annotate(similarity=SearchRank(vectorContacts, que)).exclude(similarity__lte = 0).aggregate(Sum('similarity'))
                    dAgency_sum = Agency.objects.filter(id_fk=entry).annotate(similarity=SearchRank(vectorAgency, que)).exclude(similarity__lte = 0).aggregate(Sum('similarity'))
                    dDep_sum = Department.objects.filter(id_fk=entry).annotate(similarity=SearchRank(vectorDepartment, que)).exclude(similarity__lte = 0).aggregate(Sum('similarity'))
                    if dContacts_sum['similarity__sum'] is None:
                        dContacts_sum['similarity__sum'] = 0
                    if dAgency_sum['similarity__sum'] is None:
                        dAgency_sum['similarity__sum'] = 0
                    if dDep_sum['similarity__sum'] is None:
                        dDep_sum['similarity__sum'] = 0
                    entry.rank += round((dContacts_sum.get('similarity__sum') + dAgency_sum.get('similarity__sum') + dDep_sum.get('similarity__sum')) * settings.factorText, 4)
                    if entry.rank >= settings.filterGTE:
                        if dominantEssence == "territory":
                            entry.rank += settings.factorPage
                        result_dict['/territory/' + str(entry.id)] = {
                            'id': entry.id,
                            'rank': entry.rank,
                            'title': entry.title,
                            'titlePreview': None,
                            'type': 'territory'
                        }
            # =====================================================================================================
            # =================================== Search query inside Trends ======================================
            # =====================================================================================================
            vectorContacts = SearchVector('name') + SearchVector('position')
            vectorTitle = SearchVector('title')
            vectorText = SearchVector('text')
            for word in query_dict:
                que = SearchQuery(word)
                trends_temp = Trends.objects.annotate(qTitle=SearchRank(vectorTitle, que), qText = SearchRank(vectorText, que))
                for entry in trends_temp:
                    entry.rank = round(entry.qTitle * settings.factorTitle + entry.qText * settings.factorText, 4)
                    tContacts_sum = TrendsContacts.objects.filter(id_fk=entry).annotate(similarity=SearchRank(vectorContacts, que)).exclude(similarity__lte = 0).aggregate(Sum('similarity'))
                    if tContacts_sum['similarity__sum'] is None:
                        tContacts_sum['similarity__sum'] = 0
                    entry.rank += round(tContacts_sum.get('similarity__sum') * settings.factorText, 4)
                    if entry.rank >= settings.filterGTE:
                        if dominantEssence == "direction":
                            entry.rank += settings.factorPage
                        result_dict['/direction/' + str(entry.id)] = {
                            'id': entry.id,
                            'rank': entry.rank,
                            'title': entry.title,
                            'titlePreview': None,
                            'type': 'direction'
                        }

        founded_content = ResultDictBuilder(result_dict)
        count_content = len(founded_content)
        return Response({
            "data": founded_content[offset:offset + 12],
            "count": count_content,
       })
