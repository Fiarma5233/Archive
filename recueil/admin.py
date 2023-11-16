from django.contrib import admin
from .models import *


# Register your models here.

class YearModelAdmin(admin.ModelAdmin):
    list_display=('nom', 'periode', 'date')


class SemestreModelAdmin(admin.ModelAdmin):
    list_display = ('year', 'nom', 'date')

class ModuleModelAdmin(admin.ModelAdmin):
    list_display = ('semestre', 'nom' ,  'date')


class FichierModelAdmin(admin.ModelAdmin):
    list_display = ('module', 'get_file_name', 'status', 'date')


admin.site.register(Year, YearModelAdmin)

admin.site.register(Semestre, SemestreModelAdmin)

admin.site.register(Module, ModuleModelAdmin)

admin.site.register(Fichier, FichierModelAdmin)



