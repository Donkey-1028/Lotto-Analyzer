from django.urls import path

from .views import ShowLottoCount, home

app_name = 'analyzer'

urlpatterns = [
    path('home/', home, name='home'),
    path('show/<pk>/', ShowLottoCount.as_view(), name='show_lotto_count'),
]