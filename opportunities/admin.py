from django.contrib import admin
from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminMixin
from .models import Opportunities, OpportunitiesBlock, OpportunitiesFile
from tabbed_admin import TabbedModelAdmin
from django.utils import dateformat
from django.urls import reverse
from django.utils.safestring import mark_safe
from datetime import timedelta
from home.settings import DATE_FORMAT, MONTH_FORMAT
from EngRuDate import month_from_ru_to_eng
from image_cropping import ImageCroppingMixin

# Register your models here.


class OpportunitiesFileInline(admin.StackedInline):
    model = OpportunitiesFile
    readonly_fields = ['imagePreView', "return_back"]
    extra = 1
    fields = ["file", "label", "return_back"]
    def return_back(self, obj):
        if obj.pk:
            url = reverse( 'admin:%s_%s_change' % (obj._meta.app_label, obj.id_fk.id_fk._meta.model_name), args=[obj.id_fk.id_fk.pk,])
            return mark_safe('<b><a style="color: #090;" href="{url}">{text}</a></b>'.format(
                url=url+"#tabs-2",
                text=('Вернуться к редактированию Блоков')
            ))
        return ""
    return_back.short_description = ""
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(OpportunitiesBlock)
class OpportunitiesBlockAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = ["topLine", "title", "text", "bottomLine", ]
    inlines = [OpportunitiesFileInline]
    def get_model_perms(self, request):
        return {}

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save'] = False
        return super(OpportunitiesBlockAdmin, self).changeform_view(request, object_id, extra_context=extra_context)
class OpportunitiesBlocksInline(SortableInlineAdminMixin,admin.StackedInline):
    model = OpportunitiesBlock
    readonly_fields = ['get_edit_link']
    extra = 1
    fieldsets = (
        (None, {
            'fields': ()
        }),
        ('Редактирование', {
            'classes': ('collapse',),
            'fields': ("customOrder","include","get_edit_link")
        }),
    )
    def get_edit_link(self, obj):
        if obj.pk:  # if object has already been saved and has a primary key, show link to it
            url = reverse( 'admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[obj.pk,])
            return mark_safe('<b><a style="color: #090;" href="{url}">{text}</a></b>'.format(
                url=url,
                text=('Кликните по Этой ссылке для редактирования блока')
            ))
        return mark_safe('<b style="color: #900;"> Создайте элемент и отредактируйте его после!!</b>')
    get_edit_link.short_description = "Редактировать блок"
def reverse_date(modeladmin, request, queryset):
    for flagman in queryset:
        if flagman.dateStart is None:
            flagman.dateStart = flagman.dateEnd
            flagman.save()
reverse_date.short_description = "Реверсировать одиночные даты"
class OpportinitiesAdmin(ImageCroppingMixin,admin.ModelAdmin):
    model = Opportunities
    list_display = ['title', 'date', 'main']
    readonly_fields = ('to_blocks','date')
    actions = [reverse_date]
    inlines = [OpportunitiesBlocksInline]
    fieldsets = (
        (None, {
            'fields': ('to_blocks',),
        }),
        ("Основная информация", {
            'fields': ('title', 'main'),
        }),
        ("Изображения", {
            'fields': ('imageOld', ('image', 'imageBig'), 'checkTitle'),
        }),
        ("Дополнительная информация", {
            'fields': (('address', 'map'), 'time', ('dateStart','dateEnd') ,'date','trends',),
        }),
    )
    def to_blocks(self, obj):
        if obj.pk:  # if object has already been saved and has a primary key, show link to it
            url = reverse( 'admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[obj.pk,])
            return mark_safe('<b><a style="color: #090;" href="{url}">{text}</a></b>'.format(
                url=url+"#opportunitiesblock_set-group",
                text=('Перейти к блокам')
            ))
        url = reverse('admin:%s_%s_add' % (obj._meta.app_label, obj._meta.model_name))
        return mark_safe('<b><a style="color: #090;" href="{url}">{text}</a></b>'.format(
            url=url+"#opportunitiesblock_set-group",
            text=('Перейти к блокам')
        ))
    to_blocks.short_description = ""

    def save_model(self, request, obj, form, change):
        if obj.dateEnd is None:
            if obj.dateStart is None:
                obj.date = ""
            else:
                obj.dateEnd = obj.dateStart
                obj.date = dateformat.format(obj.dateEnd, DATE_FORMAT)
        else:
            if obj.dateStart is None:
                obj.date = ""
            else:
                if obj.dateEnd < obj.dateStart:
                    obj.dateStart = obj.dateEnd
                prev = obj.dateStart - timedelta(days=1)
                next = obj.dateEnd + timedelta(days=1)
                if prev.month is not obj.dateStart.month and next.month is not obj.dateEnd.month:
                    if obj.dateStart.month == obj.dateEnd.month and obj.dateStart.year == obj.dateEnd.year:
                        obj.date = month_from_ru_to_eng(dateformat.format(obj.dateEnd, MONTH_FORMAT)) + " " + obj.dateEnd.strftime("%Y")
                    else:
                        obj.date = obj.dateStart.strftime("%d.%m.%Y") + " - " + obj.dateEnd.strftime("%d.%m.%Y")
                else:
                    obj.date = obj.dateStart.strftime("%d.%m.%Y") + " - " + obj.dateEnd.strftime("%d.%m.%Y")

        if obj.address is not None and obj.address != "":
            if obj.map is not None and obj.map != "":
                obj.save()
        else:
            obj.save()

    def delete_queryset(self, request, queryset):
        import shutil, os
        for obj in queryset:
            path = './media/{0}/{1}'.format(obj._meta.app_label, obj.id)
            if os.path.exists(path):
                shutil.rmtree(path, ignore_errors = True)
            obj.delete()
admin.site.register(Opportunities, OpportinitiesAdmin)
