from django.contrib import admin

from .models import Historico, Sequencia


class HistoricoAdmin(admin.ModelAdmin):
    list_display = ['identificador','create_at', 'hour', 'minute', 'color', 'numero']
    

class SequenciaAdmin(admin.ModelAdmin):
    list_display = ['p1','p2','p3','p4','p5','result',]
    

admin.site.register(Historico, HistoricoAdmin)
admin.site.register(Sequencia, SequenciaAdmin)


# Register your models here.
