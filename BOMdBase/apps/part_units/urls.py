from django.urls import path

from .views import part_units
from .views import part_units_edit
from .views import part_units_delete

urlpatterns = [
    path('part_units/', part_units, name='part_units'),
    path('part_units/edit/', part_units_edit, name='part_units_edit'),
    path('part_units/delete/', part_units_delete, name='part_units_delete')
]