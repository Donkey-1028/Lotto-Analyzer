import datetime

from django.contrib import admin
from django.shortcuts import redirect, render
from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.utils import timezone

from .models import LottoCount


current = timezone.localtime(timezone.now()).date()
result = datetime.datetime(2002, 12, 7).date()
DRWNO = (current - result) // 7


def update_new_lotto_action(modeladmin, request, queryset):
    """ 최신 Lotto 번호 update action"""
    for query in queryset:
        LottoCount.objects.update_new_lotto(query.id, DRWNO)
        model = LottoCount.objects.get(id=query.id)
        model.update_first_and_final()


update_new_lotto_action.short_description = 'Update No.%d Lotto Count' % (DRWNO.days + 1)


class LottoCountAdminManager(admin.ModelAdmin):
    list_display = ['id', 'first_drwNo', 'final_drwNo']
    change_list_template = 'admin/change_list_template.html'
    actions = [update_new_lotto_action]

    def get_urls(self):
        """ 기존의 Admin URL에 새롭게 만든 Admin View의 URl을 추가하기위해
        get_urls 메서드 오버라이딩"""
        urls = super().get_urls()
        my_urls = [
            path('create_lotto/', self.create_lotto, name='create_lotto'),
            path('create_index/', self.create_index, name='create_index'),
            path('update_index/', self.update_index, name='update_index'),
            path('update_lotto/', self.update_lotto, name='update_lotto'),
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

    @method_decorator(staff_member_required)
    def update_index(self, request):
        lottos = LottoCount.objects.all()
        return render(request, 'admin/update.html', {'lottos': lottos})

    @method_decorator(staff_member_required)
    def update_lotto(self, request):
        lotto_id = request.GET.get('lotto_id', None)
        drwNo = request.GET.get('drwNo')
        model = LottoCount.objects.update_new_lotto(lotto_id, int(drwNo))
        model.update_first_and_final()
        return redirect('admin:analyzer_lottocount_changelist')


admin.site.register(LottoCount, LottoCountAdminManager)
# Register your models here.
