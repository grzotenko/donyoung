from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Trends, TrendsContacts, TrendsDocuments, TrendsPartners, TrendsHrefs
from tabbed_admin import TabbedModelAdmin
from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminMixin
# Register your models here.
class TrendsContactsInline(SortableInlineAdminMixin,admin.StackedInline):
    model = TrendsContacts
    readonly_fields = ['imagePreView', ]
    extra = 1
    fieldsets = (
        (None, {
            'fields': ()
        }),
        ('Редактирование', {
            'classes': ('collapse',),
            'fields': ("name", "position", "image","imagePreView", "phone", "email","customOrder")
        }),
    )
class TrendsPartnersInline(SortableInlineAdminMixin,admin.StackedInline):
    model = TrendsPartners
    readonly_fields = ['imagePreView', ]
    extra = 1
    fieldsets = (
        (None, {
            'fields': ()
        }),
        ('Редактирование', {
            'classes': ('collapse',),
            'fields': ("title", "url","image","imagePreView","customOrder")
        }),
    )

class TrendsDocumentsInline(SortableInlineAdminMixin,admin.StackedInline):
    model = TrendsDocuments
    readonly_fields = []
    extra = 1
    fieldsets = (
        (None, {
            'fields': ()
        }),
        ('Редактирование', {
            'classes': ('collapse',),
            'fields': ("title", "file", "customOrder")
        }),
    )
class TrendsHrefsInline(SortableInlineAdminMixin,admin.StackedInline):
    model = TrendsHrefs
    readonly_fields = []
    extra = 1
    fieldsets = (
        (None, {
            'fields': ()
        }),
        ('Редактирование', {
            'classes': ('collapse',),
            'fields': ("title", "url", "customOrder")
        }),
    )

class TrendsAdmin(SortableAdminMixin, TabbedModelAdmin):
    model = Trends
    list_display = ['title',]
    readonly_fields = ('imagePreView',)
    tab_overview = (
        (None, {
            'fields': ('title', 'text', 'imageActive','imageInactive', 'imagePreView',),
        }),
    )
    tab_contacts = (
        TrendsContactsInline,
    )
    tab_partners = (
        TrendsPartnersInline,
    )
    tab_documents = (
        TrendsDocumentsInline,
    )
    tab_hrefs = (
        TrendsHrefsInline,
    )
    tabs = [
        ('Основная информация о направлении', tab_overview),
        ('Контакты', tab_contacts),
        ('Партнеры', tab_partners),
        ('Документы', tab_documents),
        ('Иные ссылки', tab_hrefs),
    ]
admin.site.register(Trends, TrendsAdmin)