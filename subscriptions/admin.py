from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Subs
# Register your models here.
@admin.register(Subs)
class SubsAdmin(ImportExportModelAdmin):
    pass