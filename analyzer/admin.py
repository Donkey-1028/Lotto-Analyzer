import datetime

from django.contrib import admin
from django.shortcuts import redirect, render
from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.utils import timezone

from .models import LottoCount


def update_new_lotto_action(modeladmin, request, queryset):
    """ 최신 Lotto 번호 update action
    현재 날짜와 Lotto가 시작한 날짜를 뺀후 해당 값을 7로 나누면 최신의 회차가 나옴"""
    now_date = timezone.localtime(timezone.now()).date()
    lotto_start_date = datetime.datetime(2002, 12, 7).date()
    subtract = (now_date - lotto_start_date) // 7

    DRWNO = 0
    if now_date.weekday() == 5:
        """ 토요일이 될 경우 자연스레 다음 회차를 구하게 되는데.
        토요일이 되자마자 다음회차가 나오는것이 아니기 때문에.
        즉 lotto 추첨이 되지 않은 오후8시 이전에는 기존 회차에 +1 을 할 경우
        에러가 발생, 그러한 경우 예외 처리"""
        DRWNO = subtract.days
    else:
        DRWNO = subtract.days+1

    for query in queryset:
        LottoCount.objects.update_new_lotto(query.id, DRWNO)
        model = LottoCount.objects.get(id=query.id)
        model.update_first_and_final()


update_new_lotto_action.short_description = 'Update New Lotto Count'


class LottoCountAdminManager(admin.ModelAdmin):
    list_display = ['id', 'first_drwNo', 'final_drwNo', 'get_len_drwNos']
    change_list_template = 'admin/change_list_template.html'
    actions = [update_new_lotto_action]

    def get_len_drwNos(self, obj):
        """ 첫번째 회차 번호화 마지막 회차 번호로만으로는 몇개의 회차가 포함된 Count인지 구분하기 어려움.
        이를 극복하기 위해 drwNos의 길이를 통해 업데이트 된 회차가 몇개인지 출력."""
        return len(obj.drwNos)
    get_len_drwNos.short_description = 'Count된 회차 갯수'

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
