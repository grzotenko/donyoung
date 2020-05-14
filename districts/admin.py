from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import District, DistrictMain, Agency,DistrictContacts, Department
from tabbed_admin import TabbedModelAdmin
from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminMixin
# Register your models here.

class DistrictContactsInline(SortableInlineAdminMixin,admin.StackedInline):
    model = DistrictContacts
    readonly_fields = ['imagePreView', ]
    extra = 1
    fieldsets = (
        (None, {
            'fields': ()
        }),
        ('Редактирование', {
            'classes': ('collapse',),
            'fields': ("department","name", "position", "image","imagePreView", "phone", "email","customOrder")
        }),
    )
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        field = super(DistrictContactsInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
        field.queryset = field.queryset.filter(id_fk = request._obj_)
        return field
class DepartmentInline(SortableInlineAdminMixin,admin.StackedInline):
    model = Department
    extra = 1

class AgencyInline(SortableInlineAdminMixin,admin.StackedInline):
    model = Agency
    readonly_fields = ['imagePreView', 'return_back']
    extra = 1
    fieldsets = (
        (None, {
            'fields': ()
        }),
        ('Редактирование', {
            'classes': ('collapse',),
            'fields': ("title", "text", "image","imagePreView","customOrder", )
        }),
        (None, {
            'fields': ("return_back",)
        }),
    )
    def return_back(self, obj):
        if obj.pk:
            url = reverse( 'admin:%s_%s_change' % (obj._meta.app_label, obj.id_fk.id_fk._meta.model_name), args=[obj.id_fk.id_fk.pk,])
            return mark_safe('<b><a style="color: #090;" href="{url}">{text}</a></b>'.format(
                url=url+"#tabs-2",
                text=('Вернуться к редактированию Территорий')
            ))
        return ""
    return_back.short_description = ""


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = ["title"]
    inlines = [DepartmentInline, DistrictContactsInline,AgencyInline]

    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def get_model_perms(self, request):
        return {}
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save'] = False
        return super(DistrictAdmin, self).changeform_view(request, object_id, extra_context=extra_context)
    def get_form(self, request, obj=None, **kwargs):
        # just save obj reference for future processing in Inline
        request._obj_ = obj
        return super(DistrictAdmin, self).get_form(request, obj, **kwargs)
class DistrictInline(admin.StackedInline):
    model = District
    readonly_fields = ['get_edit_link']
    extra = 1
    fieldsets = (
        (None, {
            'fields': ()
        }),
        ('Редактирование', {
            'classes': ('collapse',),
            'fields': ("title", "url", "phone", "address", "map","email", "vk", "instagram", "facebook", "isCity", "isMainCity", "countYouth", "percentageYouth", "image", "get_edit_link")
        }),
    )
    def save_model(self, request, obj, form, change):
        if obj.address is not None and obj.address != "":
            if obj.map is not None and obj.map != "":
                obj.save()
        else:
            obj.save()
    def get_edit_link(self, obj):
        if obj.pk:  # if object has already been saved and has a primary key, show link to it
            url = reverse( 'admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[obj.pk,])
            return mark_safe('<b><a style="color: #090;" href="{url}">{text}</a></b>'.format(
                url=url,
                text=('Кликните по Этой ссылке для редактирования блока "%s" ("%s")') % (obj.title, obj._meta.verbose_name)
            ))
        return mark_safe('<b style="color: #900;"> Создайте элемент и отредактируйте его после!!</b>')
    get_edit_link.short_description = "Редактировать Контакты и Органы у данной Территории"


class DistrictMainAdmin(TabbedModelAdmin):
    model = DistrictMain
    list_display = ['title',]

    def has_add_permission(self, request):
        return False if self.model.objects.count() > 0 else super().has_add_permission(request)
    def has_delete_permission(self, request, obj=None):
        return False
    tab_overview = (
        (None, {
            'fields': ('title',),
        }),
    )
    tab_districts = (
        DistrictInline,
    )
    tabs = [
        ('Основная информация о территориях', tab_overview),
        ('Все территории', tab_districts),
    ]
admin.site.register(DistrictMain, DistrictMainAdmin)
