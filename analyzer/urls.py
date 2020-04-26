from django.urls import path

from .views import Index, show_all_lotto_count

app_name = 'analyzer'

urlpatterns = [
    path('all/', show_all_lotto_count, name='all'),
    path('index/', Index.as_view(), name='index'),
]