from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import News, NewsBlock, NewsFile
from tabbed_admin import TabbedModelAdmin
from image_cropping import ImageCroppingMixin

from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminMixin
# Register your models here.

class NewsBlockFileInline(admin.StackedInline):
    model = NewsFile
    readonly_fields = ['imagePreView', "return_back"]
    extra = 1
    fields = ["file", "label", "return_back"]
    def return_back(self, obj):
        if obj.pk:
            url = reverse( 'admin:%s_%s_change' % (obj._meta.app_label, obj.id_fk.id_fk._meta.model_name), args=[obj.id_fk.id_fk.pk,])
            return mark_safe('<b><a style="color: #090;" href="{url}">{text}</a></b>'.format(
                url=url+"#newsblock_set-group",
                text=('Вернуться к редактированию Блоков')
            ))
        return ""
    return_back.short_description = ""
    def has_delete_permission(self, request, obj=None):
        return False
# from ckeditor.widgets import CKEditorWidget
# from django import forms
# class NewsBlockAdminForm(forms.ModelForm):
#     text = forms.CharField(widget=CKEditorWidget())
#     class Meta:
#         model = NewsBlock
#         fields = ["topLine", "title", "text", "bottomLine"]

@admin.register(NewsBlock)
class NewsBlockAdmin(admin.ModelAdmin):
    save_on_top = True
    # form = NewsBlockAdminForm
    fields = ["topLine", "title", "text", "bottomLine", ]
    inlines = [NewsBlockFileInline]
    def get_model_perms(self, request):
        return {}
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save'] = False
        return super(NewsBlockAdmin, self).changeform_view(request, object_id, extra_context=extra_context)

class NewsBlockInline(SortableInlineAdminMixin,admin.StackedInline):
    model = NewsBlock
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

class NewsAdmin(ImageCroppingMixin,admin.ModelAdmin):
    model = News
    list_display = ['title', 'date', 'main', 'important']
    readonly_fields = ()
    inlines = [NewsBlockInline]
    fieldsets = (
        ("Основная информация", {
            'fields': ('title', 'titlePreview', 'date',),
        }),
        ("Изображения", {
            'fields': ('imageOld', ('image', 'imageBig')),
        }),
        ("Дополнительная информация", {
            'fields': (('main', 'important'), 'trends',),
        }),
    )
    def save_model(self, request, obj, form, change):
        if obj.main:
            obj.important = False
        obj.save()

    def delete_queryset(self, request, queryset):
        import shutil, os
        for obj in queryset:
            path = './media/{0}/{1}'.format(obj._meta.app_label, obj.id)
            if os.path.exists(path):
                shutil.rmtree(path, ignore_errors = True)
            obj.delete()
admin.site.register(News, NewsAdmin)
