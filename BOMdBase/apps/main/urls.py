from django.urls import path

from .views import main
from .backup import backup
from .restore import restore

urlpatterns = [
    path('', main, name='main'),
    path('main/', main, name='main'),
    path('backup/', backup, name='backup'),
    path('restore/', restore, name='restore'),
]