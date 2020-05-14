from django.contrib import admin
from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminMixin
from .models import About,AboutBlock,AboutBlockPeople
from tabbed_admin import TabbedModelAdmin
from django.urls import reverse
from django.utils.safestring import mark_safe
# Register your models here.

class AboutBlockPeopleAdmin(SortableInlineAdminMixin,admin.StackedInline):
    model = AboutBlockPeople
    readonly_fields = ['imagePreView']
    extra = 1
    fieldsets = (
        (None, {
            'fields': ()
        }),
        ('Редактирование', {
            'classes': ('collapse',),
            'fields': ("id", "position", "name", "phone",'image' ,"email","customOrder")
        }),
    )

@admin.register(AboutBlock)
class AboutAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = ["title"]
    inlines = [AboutBlockPeopleAdmin]

    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def get_model_perms(self, request):
        return {}


class AboutBlocksInline(SortableInlineAdminMixin,admin.StackedInline):
    model = AboutBlock
    readonly_fields = ['get_edit_link']
    extra = 1
    fieldsets = (
        (None, {
            'fields': ()
        }),
        ('Редактирование', {
            'classes': ('collapse',),
            'fields': ("title", "customOrder",'get_edit_link')
        }),
    )
    def get_edit_link(self, obj):
        if obj.pk:  # if object has already been saved and has a primary key, show link to it
            url = reverse( 'admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[obj.pk,])
            return mark_safe('<b><a style="color: #090;" href="{url}">{text}</a></b>'.format(
                url=url,
                text=('Кликните по Этой ссылке для редактирования блока "%s" ("%s")') % (obj.title, obj._meta.verbose_name)
            ))
        return mark_safe('<b style="color: #900;"> Создайте элемент и отредактируйте его после!!</b>')
    get_edit_link.short_description = "Редактировать контакты"


class AboutAdmin(TabbedModelAdmin):
    model = About
    # readonly_fields = ('imagePreView',)
    tab_overview = (
        (None, {
            'fields': ('text', 'email', 'phone', 'map', 'address', 'work_time',),
        }),
    )
    tab_news_block = (
        AboutBlocksInline,
    )
    tabs = [
        ('Основная информация', tab_overview),
        ('Блоки Отделов', tab_news_block),
    ]
    def save_model(self, request, obj, form, change):
        if obj.address is not None and obj.address != "":
            if obj.map is not None and obj.map != "":
                obj.save()
        else:
            obj.save()
    def has_add_permission(self, request):
        return False if self.model.objects.count() > 0 else super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False
admin.site.register(About, AboutAdmin)
