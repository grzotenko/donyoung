from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import MediaFiles, MediaPhotos,MediaVideos
from tabbed_admin import TabbedModelAdmin
from django.urls import reverse
from django.utils.safestring import mark_safe
from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminMixin, SortableAdminBase
from image_cropping import ImageCroppingMixin

# Register your models here.
class MediaPhotosInline(SortableInlineAdminMixin,admin.StackedInline):
    model = MediaPhotos
    readonly_fields = ['get_edit_link']
    extra = 1
    fieldsets = (
        (None, {
            'fields': ()
        }),
        ('Редактирование', {
            'classes': ('collapse',),
            'fields': ("customOrder","title","get_edit_link")
        }),
    )
    def get_edit_link(self, obj):
        if obj.pk:  # if object has already been saved and has a primary key, show link to it
            url = reverse( 'admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[obj.pk,])
            return mark_safe('<b><a style="color: #090;" href="{url}">{text}</a></b>'.format(
                url=url,
                text=('Кликните по Этой ссылке для редактирования фотоальбома')
            ))
        return mark_safe('<b style="color: #900;"> Создайте элемент и отредактируйте его после!!</b>')
    get_edit_link.short_description = "Редактировать фотоальбом"
@admin.register(MediaPhotos)
class MediaPhotosAdmin(ImageCroppingMixin, admin.ModelAdmin):
    fields = ["title","url", "imageOld", "image"]

    def get_model_perms(self, request):
        return {}

    def delete_queryset(self, request, queryset):
        import shutil, os
        for obj in queryset:
            path = './media/{0}/{1}'.format(obj._meta.app_label, obj.id)
            if os.path.exists(path):
                shutil.rmtree(path)
            obj.delete()
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save'] = False
        return super(MediaPhotosAdmin, self).changeform_view(request, object_id, extra_context=extra_context)

class MediaVideosInline(SortableInlineAdminMixin,admin.StackedInline):
    model = MediaVideos
    readonly_fields = []
    extra = 1
    fieldsets = (
        (None, {
            'fields': ()
        }),
        ('Редактирование', {
            'classes': ('collapse',),
            'fields': ("title","url", "customOrder")
        }),
    )
class MediaFilesAdmin(TabbedModelAdmin):
    model = MediaFiles
    list_display = ['title', 'urlPhotos','urlVideos']
    tab_overview = (
        (None, {
            'fields': ('title', 'urlPhotos', 'urlVideos',),
        }),
    )
    tab_photos = (
        MediaPhotosInline,
    )
    tab_videos = (
        MediaVideosInline,
    )
    tabs = [
        ('Основная информация', tab_overview),
        ('Фотоальбомы', tab_photos),
        ('Видео', tab_videos),
    ]
    def has_add_permission(self, request):
        return False if self.model.objects.count() > 0 else super().has_add_permission(request)
    def has_delete_permission(self, request, obj=None):
        return False
admin.site.register(MediaFiles, MediaFilesAdmin)