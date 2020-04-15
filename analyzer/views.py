from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic.base import View
from django.views.generic.detail import DetailView

from .models import LottoCount


class UpdateNewLotto(View):
    def get(self, request, *args, **kwargs):
        LottoCount.objects.update_new_lotto(2, 1)
        LottoCount.objects.create_many_lotto_count(10)

        return render(request, 'test.html')  # 하드코딩 되어 있음


class CreateManyLottoCount(View):
    def get(self, request, *args, **kwargs):
        LottoCount.objects.create_many_lotto_count(906)
        return redirect('/')  # render 할 경우 반환시간 만료 발생. 수정이 필요해 보인다


class ShowLottoCount(DetailView):
    model = LottoCount
    template_name = 'index.html'
