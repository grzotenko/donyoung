from django.contrib import admin
from .models import Main, HeaderMenu, HeaderOrganizers, SocialNet, FooterContacts, FooterPartners
from searchdon.models import SettingsSearch
from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminMixin
from tabbed_admin import TabbedModelAdmin
from django.urls import reverse
from django.utils.safestring import mark_safe
from image_cropping import ImageCroppingMixin
# Register your models here.
from django.contrib.admin.templatetags.admin_modify import register, submit_row as original_submit_row

@register.inclusion_tag('admin/submit_line.html', takes_context=True)
def submit_row(context):
    ctx = original_submit_row(context)
    ctx.update({
        'show_save_and_add_another': context.get('show_save_and_add_another',
                                                 ctx['show_save_and_add_another']),
        'show_save_and_continue': context.get('show_save_and_continue',
                                              ctx['show_save_and_continue']),
        'show_save': context.get('show_save',
                                 ctx['show_save']),
        'show_delete_link': context.get('show_delete_link', ctx['show_delete_link'])
    })
    return ctx




class HeaderMenuInline(admin.StackedInline):
    model = HeaderMenu
    # readonly_fields = ["path"]
    extra = 0
    fields = ['title', 'path']

    def has_add_permission(self, request):
        return False if self.model.objects.count() > 7 else super().has_add_permission(request)

class HeaderOrganizersInline(SortableInlineAdminMixin,admin.StackedInline):
    model = HeaderOrganizers
    extra = 1
    fields = ["url","image","customOrder"]
    def has_add_permission(self, request):
        return False if self.model.objects.count() > 5 else super().has_add_permission(request)

class SocialNetInline(admin.StackedInline):
    model = SocialNet
    extra = 0
    fields = ['vk', 'youtube', 'facebook', 'instagram', ]

    def has_add_permission(self, request):
        return False if self.model.objects.count() > 0 else super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False


class FooterContactsInline(admin.StackedInline):
    model = FooterContacts
    readonly_fields = []
    extra = 0
    fields = ['title', 'phone', 'email','address','map']

    def has_add_permission(self, request):
        return False if self.model.objects.count() > 1 else super().has_add_permission(request)
    def has_delete_permission(self, request, obj=None):
        return False
@admin.register(FooterPartners)
class FooterPartnersAdmin(ImageCroppingMixin, admin.ModelAdmin):
    fields = ["imageOld", "image", "return_back"]
    readonly_fields = ["return_back",]
    def return_back(self, obj):
        if obj.pk:
            url = '/admin/main/main/1/change/#tabs-6'
            return mark_safe('<b><a style="color: #090;" href="{url}">{text}</a></b>'.format(
                url=url,
                text=('Вернуться к редактированию Партнеров')
            ))
        return ""
    return_back.short_description = ""
    def get_model_perms(self, request):
        return {}

    def delete_queryset(self, request, queryset):
        import shutil, os
        for obj in queryset:
            path = './media/{0}/{1}/{2}'.format(obj._meta.app_label, obj._meta.model_name, obj.id)
            if os.path.exists(path):
                shutil.rmtree(path)
            obj.delete()

class FooterPartnersInline(SortableInlineAdminMixin,admin.StackedInline):
    model = FooterPartners
    extra = 1
    readonly_fields = ["get_edit_link",]
    fields = ["url","get_edit_link","customOrder"]
    def get_edit_link(self, obj):
        if obj.pk:  # if object has already been saved and has a primary key, show link to it
            url = reverse( 'admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[obj.pk,])
            return mark_safe('<b><a style="color: #090;" href="{url}">{text}</a></b>'.format(
                url=url,
                text=('Кликните по Этой ссылке для редактирования картинки')
            ))
        return mark_safe('<b style="color: #900;"> Создайте элемент и отредактируйте его после!!</b>')
    get_edit_link.short_description = "Редактировать картинку"
class SettingsSearchInline(admin.StackedInline):
    model = SettingsSearch
    fields = ["factorTitle","factorPreview","factorText", "factorPage","filterGTE", "rank_similarity"]
    radio_fields = {"rank_similarity": admin.HORIZONTAL}
    extra = 0
    def has_add_permission(self, request):
        return False if self.model.objects.count() > 0 else super().has_add_permission(request)
    def has_delete_permission(self, request, obj=None):
        return False
class MainAdmin(TabbedModelAdmin):
    model = Main
    tab_overview = (
        (None, {
            'fields': ('banner', 'logo','copyright'),
        }),
    )
    tab_menu = (
        HeaderMenuInline,
    )
    tab_organizers = (
        HeaderOrganizersInline,
    )
    tab_socialnet = (
        SocialNetInline,
    )
    tab_contacts = (
        FooterContactsInline,
    )
    tab_partners = (
        FooterPartnersInline,
    )
    tab_search = (
        SettingsSearchInline,
    )
    tabs = [
        ('Общая информация', tab_overview),
        ('Меню', tab_menu),
        ('Организаторы', tab_organizers),
        ('Социальные сети', tab_socialnet),
        ('Контакты', tab_contacts),
        ('Партнеры', tab_partners),
        ('Настройки поиска', tab_search),
    ]

    def has_add_permission(self, request):
        return False if self.model.objects.count() > 0 else super().has_add_permission(request)
admin.site.register(Main, MainAdmin)
