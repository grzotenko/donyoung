from django.shortcuts import render, get_object_or_404
from .models import *
from .serializers import *
from rest_framework import views
from rest_framework.response import Response
from datetime import date
# Create your views here.
class FlagmansActiveViewSet(views.APIView):
    def get(self, request, page):
        offset = int(page)
        serializerFlagmans = FlagmansSerializer(Flagmans.objects.filter(dateEnd__gte = date.today())[offset:offset+12], many=True)
        return Response(dataFlagmans(serializerFlagmans))

class FlagmansCompletedViewSet(views.APIView):
    def get(self, request, page):
        offset = int(page)
        serializerFlagmans = FlagmansSerializer(Flagmans.objects.filter(dateEnd__lt = date.today())[offset:offset+12], many=True)
        return Response(dataFlagmans(serializerFlagmans))
from districts.models import *
def dataFlagmans(serializerFlagmans):
    dataFlagman = serializerFlagmans.data
    from image_cropping.utils import get_backend
    for flagman in dataFlagman:
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
    import docx

    doc = docx.Document('testgovno.docx')
    table = doc.tables[0]
    countDistr = 0
    countPos = 0
    countName = 0
    countPhone = 0
    countMail = 0

    i = 0
    prevDistr = table.rows[1].cells[9].text
    prevPos = table.rows[3].cells[100].text
    POS = ["Начальник", "Специалист", "Старший", "Ведущий", "Главный", "Заведующий", "Директор", "Заместитель", "Художественный", "Инспектор", "специалист"]
    prevName = table.rows[4].cells[0].text
    prevPhone = table.rows[3].cells[15].text
    prevMail = table.rows[3].cells[20].text
    exitFlag = False
    for row in table.rows:
        for cell in row.cells:
            if i == 0:
                if cell.text.find("г. ") >= 0 or cell.text.find("РАЙОН") >= 0:
                    text = cell.text.strip().replace("г. ", "").capitalize()
                    print("0")
                    print(text)
                    try:
                        d = District.objects.get(title=text)
                        i = 1
                        print(d)
                    except:
                        pass
            elif i == 1:
                text = cell.text.strip()
                if text.split(" ")[0] in POS:
                    try:
                        print("1")
                        i = 2
                        prevPos = cell.text
                        txt = prevPos.strip()
                        con = DistrictContacts(id_fk=d, position=txt)
                        print(txt)
                    except:
                        pass
            elif i == 2:
                if cell.text !=prevPos:
                    try:
                        i = 3
                        print("2")
                        prevName = cell.text
                        txt = prevName.strip()
                        con.name = txt
                        print(txt)
                    except:
                        pass
            elif i == 3:
                if cell.text != prevName:
                    try:
                        i = 4
                        print("3")
                        prevPhone = cell.text
                        txt = prevPhone.strip()
                        con.phone = txt
                        print(txt)
                    except:
                        pass
            elif i == 4:
                if cell.text != prevPhone:
                    try:
                        txt = cell.text.strip()
                        con.email = txt
                        con.save()
                        print("4")
                        print(txt)
                        print(con)
                        print("________________________________________________________")
                        i = 1
                        # exitFlag = True
                        # break
                    except:
                        pass
        # if exitFlag:
        #     break
    return dataFlagman
