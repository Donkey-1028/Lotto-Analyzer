from django.contrib import admin
from .models import LottoCount


class LottoCountManager(admin.ModelAdmin):
    list_display = ['id', 'first_drwNo', 'final_drwNo']


admin.site.register(LottoCount, LottoCountManager)
# Register your models here.
