from django.shortcuts import render
from django.views.generic.detail import DetailView

from .models import LottoCount


def home(request):
    lotto = LottoCount.objects.filter(id=4).values()[0]  # 전체보기로 지정된 object
    lotto_count = [value for _, value in enumerate(lotto.values())]
    lotto_number = [value for _, value in enumerate(lotto.keys())]
    return render(request, 'home.html', {'lotto': zip(lotto_number, lotto_count)})


class ShowLottoCount(DetailView):
    model = LottoCount
    template_name = 'index.html'

