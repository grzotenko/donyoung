#!/usr/bin/env python3
import os, sys
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "home.settings")
django.setup()
from django_seed import Seed
from home.settings import DATE_FORMAT, MONTH_FORMAT
from django.utils import dateformat
from datetime import date, timedelta

def media(count):
    count = int(count)
    seeder = Seed.seeder()
    from mediafiles.models import MediaVideos, MediaFiles, MediaPhotos
    mediaMain = MediaFiles.objects.first()
    seeder.add_entity(MediaPhotos, count, {
        'id_fk': lambda x: mediaMain,
        'url': lambda x: seeder.faker.url(),
    })
    seeder.add_entity(MediaVideos, count, {
        'id_fk': lambda x: mediaMain,
        'url': lambda x: seeder.faker.url(),
    })
    inserted_pks = seeder.execute()
    from news.models import News
    lastImage = News.objects.last().image
    for idP in inserted_pks.get(MediaPhotos):
        photo = MediaPhotos.objects.get(id = idP)
        photo.image = lastImage
        photo.save()


def news(count):
    count = int(count)
    countB = count//2 if count//2 > 0 else 1
    countF = countB // 2 if countB // 2 > 0 else 1
    seeder = Seed.seeder()
    from news.models import News, NewsBlock, NewsFile
    seeder.add_entity(News, count)
    seeder.add_entity(NewsBlock, countB)
    seeder.add_entity(NewsFile, countF)
    inserted_pks = seeder.execute()
    lastImage = News.objects.last().image
    counter = 0
    from trends.models import Trends
    fTrend = Trends.objects.first()
    lTrend = Trends.objects.last()
    for idN in inserted_pks.get(News):
        news = News.objects.get(id = idN)
        news.image = lastImage
        if counter % 3 == 0:
            news.trends.add(fTrend, lTrend)
        elif counter % 3 == 1:
            news.trends.add(fTrend)
        news.save()
        counter += 1
    for idN in inserted_pks.get(NewsFile):
        newsFile = NewsFile.objects.get(id=idN)
        newsFile.file = lastImage
        newsFile.save()

def opportunitiesImage(inserted_pks):
    from news.models import News
    from opportunities.models import OpportunitiesFile, Opportunities
    lastImage = News.objects.last().image
    from trends.models import Trends
    fTrend = Trends.objects.first()
    lTrend = Trends.objects.last()
    counter = 0
    for idN in inserted_pks.get(Opportunities):
        oppo = Opportunities.objects.get(id=idN)
        oppo.image = lastImage
        if counter % 3 == 0:
            oppo.trends.add(fTrend, lTrend)
        elif counter % 3 == 1:
            oppo.trends.add(fTrend)
        oppo.save()
        counter += 1
    for idN in inserted_pks.get(OpportunitiesFile):
        oppoFile = OpportunitiesFile.objects.get(id=idN)
        oppoFile.file = lastImage
        oppoFile.save()

def opportunities1(count):
    count = int(count)
    countB = count//2 if count//2 > 0 else 1
    countF = countB // 2 if countB // 2 > 0 else 1
    seeder = Seed.seeder()
    from opportunities.models import OpportunitiesBlock, OpportunitiesFile, Opportunities
    today = date.today()
    seeder.add_entity(Opportunities, count, {
        'dateStart': lambda x: None,
        'dateEnd': lambda x: today,
        'date': lambda x: dateformat.format(today, DATE_FORMAT),
    })
    seeder.add_entity(OpportunitiesBlock, countB)
    seeder.add_entity(OpportunitiesFile, countF)
    inserted_pks = seeder.execute()
    opportunitiesImage(inserted_pks)

def opportunities2(count):
    count = int(count)
    countB = count//2 if count//2 > 0 else 1
    countF = countB // 2 if countB // 2 > 0 else 1
    seeder = Seed.seeder()
    from opportunities.models import OpportunitiesBlock, OpportunitiesFile, Opportunities
    today = date.today()
    from EngRuDate import month_from_ru_to_eng
    from calendar import monthrange
    dateS = date(year=today.year, month=today.month, day=1)
    dateE = date(year=today.year, month=today.month, day=monthrange(today.year, today.month)[1])
    dateM = month_from_ru_to_eng(dateformat.format(dateE, MONTH_FORMAT)) + " " + dateE.strftime("%Y")
    seeder.add_entity(Opportunities, count, {
        'dateStart': lambda x: dateS,
        'dateEnd': lambda x: dateE,
        'date': lambda x: dateM,
    })
    seeder.add_entity(OpportunitiesBlock, countB)
    seeder.add_entity(OpportunitiesFile, countF)
    inserted_pks = seeder.execute()
    opportunitiesImage(inserted_pks)

def opportunities3(count):
    count = int(count)
    countB = count//2 if count//2 > 0 else 1
    countF = countB // 2 if countB // 2 > 0 else 1
    seeder = Seed.seeder()
    from opportunities.models import OpportunitiesBlock, OpportunitiesFile, Opportunities
    today = date.today()
    today2 = today + timedelta(days=3)
    seeder.add_entity(Opportunities, count, {
        'dateStart': lambda x: today,
        'dateEnd': lambda x: today2,
        'date': lambda x: today.strftime("%d.%m.%Y") + " - " + today2.strftime("%d.%m.%Y"),
    })
    seeder.add_entity(OpportunitiesBlock, countB)
    seeder.add_entity(OpportunitiesFile, countF)
    inserted_pks = seeder.execute()
    opportunitiesImage(inserted_pks)

def about(count):
    count = int(count)
    countB = count//2 if count//2 > 0 else 1
    seeder = Seed.seeder()
    from about.models import About, AboutBlock, AboutBlockPeople
    from news.models import News
    lastImage = News.objects.last().image
    aboutMain = About.objects.first()
    seeder.add_entity(AboutBlock, count, {
        'id_fk': lambda x: aboutMain,
    })
    seeder.add_entity(AboutBlockPeople, countB)
    inserted_pks = seeder.execute()
    for idA in inserted_pks.get(AboutBlockPeople):
        aboutBlockPeople = AboutBlockPeople.objects.get(id=idA)
        aboutBlockPeople.image = lastImage
        aboutBlockPeople.save()

def district(count):
    count = int(count)
    countB = count*2
    seeder = Seed.seeder()
    from districts.models import District, DistrictAgency, DistrictContacts, DistrictMain
    from news.models import News
    lastImage = News.objects.last().image
    districtMain = DistrictMain.objects.first()
    seeder.add_entity(District, count, {
        'id_fk': lambda x: districtMain,
    })
    seeder.add_entity(DistrictContacts, countB)
    seeder.add_entity(DistrictAgency, countB)
    inserted_pks = seeder.execute()
    for idD in inserted_pks.get(District):
        districtO = District.objects.get(id=idD)
        districtO.image = lastImage
        districtO.save()
    for idD in inserted_pks.get(DistrictContacts):
        districtO = DistrictContacts.objects.get(id=idD)
        districtO.image = lastImage
        districtO.save()
    for idD in inserted_pks.get(DistrictAgency):
        districtO = DistrictAgency.objects.get(id=idD)
        districtO.image = lastImage
        districtO.save()

def flagmansImage(inserted_pks):
    from news.models import News
    from flagmans.models import Flagmans
    lastImage = News.objects.last().image
    for idD in inserted_pks.get(Flagmans):
        flagship = Flagmans.objects.get(id=idD)
        flagship.image = lastImage
        flagship.save()


def flagmans1(count):
    count = int(count)
    seeder = Seed.seeder()
    from flagmans.models import Flagmans
    today = date.today()
    seeder.add_entity(Flagmans, count, {
        'url': lambda x: seeder.faker.url(),
        'dateStart': lambda x: None,
        'dateEnd': lambda x: today,
        'date': lambda x: dateformat.format(today, DATE_FORMAT),
    })
    inserted_pks = seeder.execute()
    flagmansImage(inserted_pks)

def flagmans2(count):
    count = int(count)
    seeder = Seed.seeder()
    from flagmans.models import Flagmans
    today = date.today()
    from EngRuDate import month_from_ru_to_eng
    from calendar import monthrange
    dateS = date(year=today.year, month=today.month, day=1)
    dateE = date(year=today.year, month=today.month, day=monthrange(today.year, today.month)[1])
    dateM = month_from_ru_to_eng(dateformat.format(dateE, MONTH_FORMAT)) + " " + dateE.strftime("%Y")
    seeder.add_entity(Flagmans, count, {
        'url': lambda x: seeder.faker.url(),
        'dateStart': lambda x: dateS,
        'dateEnd': lambda x: dateE,
        'date': lambda x: dateM,
    })
    inserted_pks = seeder.execute()
    flagmansImage(inserted_pks)

def flagmans3(count):
    count = int(count)
    seeder = Seed.seeder()
    from flagmans.models import Flagmans
    today = date.today()
    today2 = today+timedelta(days=3)
    seeder.add_entity(Flagmans, count, {
        'url': lambda x: seeder.faker.url(),
        'dateStart': lambda x: today,
        'dateEnd': lambda x: today2,
        'date': lambda x: today.strftime("%d.%m.%Y") + " - " + today2.strftime("%d.%m.%Y"),
    })
    inserted_pks = seeder.execute()
    flagmansImage(inserted_pks)

def trends(count):
    count = int(count)
    countB = count//2 if count//2 > 0 else 1
    seeder = Seed.seeder()
    from trends.models import Trends, TrendsPartners, TrendsDocuments, TrendsContacts
    seeder.add_entity(Trends, count)
    seeder.add_entity(TrendsContacts, countB)
    seeder.add_entity(TrendsDocuments, countB)
    seeder.add_entity(TrendsPartners, countB)
    inserted_pks = seeder.execute()
    from news.models import News
    lastImage = News.objects.last().image
    for idN in inserted_pks.get(Trends):
        trend = Trends.objects.get(id = idN)
        trend.imageInactive = lastImage
        trend.imageActive = lastImage
        trend.save()
    for idN in inserted_pks.get(TrendsPartners):
        trend = TrendsPartners.objects.get(id=idN)
        trend.image = lastImage
        trend.save()
    for idN in inserted_pks.get(TrendsContacts):
        trend = TrendsContacts.objects.get(id=idN)
        trend.image = lastImage
        trend.save()
    for idN in inserted_pks.get(TrendsDocuments):
        trend = TrendsDocuments.objects.get(id=idN)
        trend.file = lastImage
        trend.save()


if __name__ == '__main__':
    globals()[sys.argv[1]](sys.argv[2])
