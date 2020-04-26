from django.shortcuts import render
from django.views.generic.base import TemplateView

from .models import LottoCount


def show_all_lotto_count(request):
    try:
        lotto = LottoCount.objects.filter(all=True).values()[0]  # 전체보기로 지정된 object
    except Exception as e:
        raise Exception('lotto filter 실패, all에 등록된 LottoCount를 확인하세요.')
    else:
        # id, first_drwNo, final_drwNo, drwNos, boolean data 는 건너 뜀.
        data = [value for index, value in enumerate(lotto.values()) if 2 < index < len(lotto.values()) - 6]
        labels = [value for index, value in enumerate(lotto.keys()) if 2 < index < len(lotto.keys()) - 6]
        count = str(lotto['first_drwNo']) + '-' + str(lotto['final_drwNo'])
        return render(request, 'all.html', {'labels': labels, 'data': data, 'count': count})


class Index(TemplateView):
    template_name = 'index.html'



