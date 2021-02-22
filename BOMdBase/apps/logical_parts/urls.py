from django.urls import path

from .views import logical_parts
from .views import logical_parts_edit
from .views import logical_parts_delete

urlpatterns = [
    path('logical_parts/', logical_parts,
        name='logical_parts'),
    path('logical_parts/edit/', logical_parts_edit,
        name='logical_parts_edit'),
    path('logical_parts/delete/', logical_parts_delete,
        name='logical_parts_delete'),
]