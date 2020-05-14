from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils import dateformat
from .models import Flagmans
from datetime import timedelta
from home.settings import DATE_FORMAT, MONTH_FORMAT
from image_cropping import ImageCroppingMixin
from EngRuDate import month_from_ru_to_eng
# Register your models here.
def reverse_date(modeladmin, request, queryset):
    for flagman in queryset:
        if flagman.dateStart is None:
            flagman.dateStart = flagman.dateEnd
            flagman.save()
reverse_date.short_description = "Реверсировать одиночные даты"
def set_none(modeladmin, request, queryset):
    for flagman in queryset:
        if flagman.dateStart == flagman.dateEnd:
            flagman.dateEnd = None
            flagman.save()
set_none.short_description = "Удалить реверсированные даты"
class FlagmansAdmin(ImageCroppingMixin, admin.ModelAdmin):
    model = Flagmans
    list_display = ['title', 'date',]
    readonly_fields = ('date',)
    actions = [reverse_date, set_none]
    def delete_queryset(self, request, queryset):
        import shutil, os
        for obj in queryset:
            path = './media/{0}/{1}'.format(obj._meta.app_label, obj.id)
            if os.path.exists(path):
                shutil.rmtree(path)
            obj.delete()
    def save_model(self, request, obj, form, change):
        if obj.dateEnd is None:
            obj.date = dateformat.format(obj.dateStart, DATE_FORMAT)
            obj.dateEnd = obj.dateStart
        else:
            if obj.dateEnd < obj.dateStart:
                obj.dateStart = obj.dateEnd
            prev = obj.dateStart - timedelta(days=1)
            next = obj.dateEnd + timedelta(days=1)
            if prev.month is not obj.dateStart.month and next.month is not obj.dateEnd.month:
                if obj.dateStart.month == obj.dateEnd.month and obj.dateStart.year == obj.dateEnd.year:
                    obj.date = month_from_ru_to_eng(
                        dateformat.format(obj.dateEnd, MONTH_FORMAT)) + " " + obj.dateEnd.strftime("%Y")
            else:
                obj.date = obj.dateStart.strftime("%d.%m.%Y") + " - " + obj.dateEnd.strftime("%d.%m.%Y")

        if obj.address is not None and obj.address != "":
            if obj.map is not None and obj.map != "":
                obj.save()
        else:
            obj.save()


    fieldsets = (
        ("Основная информация", {
            'fields': ('title', 'address', 'map', 'url'),
        }),
        ("Изображение", {
            'fields': ('imageOld', 'image'),
        }),
        ("Время проведения", {
            'fields': (('dateStart', 'dateEnd'), 'date'),
        }),
    )
admin.site.register(Flagmans, FlagmansAdmin)