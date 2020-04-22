from django.contrib import admin
from core.models import *
# Register your models here.

class StatisticsAdmin(admin.ModelAdmin):
    change_list_template = 'stats/chart.html'

# admin.site.register(StatisticsAdmin)

