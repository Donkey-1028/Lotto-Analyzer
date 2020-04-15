from django.urls import path

from .views import UpdateNewLotto, ShowLottoCount, CreateManyLottoCount

app_name = 'analyzer'

urlpatterns = [
    path('update/', UpdateNewLotto.as_view(), name='update'),
    path('create/', CreateManyLottoCount.as_view(), name='create'),
    path('show/<pk>/', ShowLottoCount.as_view(), name='show_lotto_count'),
]