from django.contrib import admin
from django.shortcuts import redirect, render
from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required

from .models import LottoCount


class LottoCountManager(admin.ModelAdmin):
    list_display = ['id', 'first_drwNo', 'final_drwNo']

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('create_lotto/', self.create_lotto, name='create_lotto'),
            path('create_index/', self.create_index, name='create_index'),
        ]
        return my_urls + urls

    @staff_member_required(login_url='admin:login')
    def create_index(self, request):
        return render(request, 'admin/create.html')

    @staff_member_required(login_url='admin:login')
    def create_lotto(self, request):
        first_drwNos = request.GET.get('first_drwNo')
        final_drwNos = request.GET.get('final_drwNo')
        LottoCount.objects.create_many_lotto_count(int(final_drwNos), int(first_drwNos))
        return redirect('admin:analyzer_lottocount_changelist')

admin.site.register(LottoCount, LottoCountManager)
# Register your models here.
