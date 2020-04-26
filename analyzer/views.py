from django.shortcuts import render
from django.views.generic.detail import DetailView

from .models import LottoCount


def home(request):
    lotto = LottoCount.objects.filter(id=4).values()[0]  # 전체보기로 지정된 object
    data = [value for index, value in enumerate(lotto.values()) if 2 < index < len(lotto.values()) - 1]
    labels = [value for index, value in enumerate(lotto.keys()) if 2 < index < len(lotto.keys()) - 1]
    return render(request, 'home.html', {'labels': labels, 'data': data})


class ShowLottoCount(DetailView):
    model = LottoCount
    template_name = 'index.html'

