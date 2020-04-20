from django.contrib import admin
from django.shortcuts import redirect, render
from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

from .models import LottoCount

DRWNO = 907  # 최신 회차 번호. 자동적으로 해당 번호를 만들어 올 수 있게 crontab 구현이 필요해보임


def update_new_lotto_action(modeladmin, request, queryset):
    """ 최신 Lotto 번호 update action"""
    for query in queryset:
        LottoCount.objects.update_new_lotto(query.id, DRWNO)
        model = LottoCount.objects.get(id=query.id)
        model.update_first_and_final()


update_new_lotto_action.short_description = 'Update No.%d Lotto Count' % DRWNO


class LottoCountAdminManager(admin.ModelAdmin):
    list_display = ['id', 'first_drwNo', 'final_drwNo']
    change_list_template = 'admin/change_list_template.html'
    actions = [update_new_lotto_action]

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('create_lotto/', self.create_lotto, name='create_lotto'),
            path('create_index/', self.create_index, name='create_index'),
        ]
        return my_urls + urls

    @method_decorator(staff_member_required)
    def create_index(self, request):
        return render(request, 'admin/create.html')

    @method_decorator(staff_member_required)
    def create_lotto(self, request):
        first_drwNos = request.GET.get('first_drwNo')
        final_drwNos = request.GET.get('final_drwNo')
        LottoCount.objects.create_many_lotto_count(int(final_drwNos), int(first_drwNos))
        return redirect('admin:analyzer_lottocount_changelist')


admin.site.register(LottoCount, LottoCountAdminManager)
# Register your models here.
